import { $ } from "bun";

// Set environment variables
const DATA_FOLDER = './data';
const SCRIPT_DIR = './src'
const AI_DIR = '/Users/gur/Documents/gurrai/src'
const model = process.env.MODEL || "gpt-4o";
const temperature = process.env.TEMPERATURE || 0.7;

async function main() {
  const video_url = process.argv[2];
  // console.log(`Processing video: ${video_url}`);

  let id = video_url;

  if (video_url.includes("youtube.com/watch?v=")) {
    const match = video_url.match(/v=([^&]+)/);
    if (match) {
      id = match[1];
    }
  }

  // console.log(`Video ID: ${id}`);

  const transcript_file = `${DATA_FOLDER}/${id}-transcript.txt`;
  const chapters_file = `${DATA_FOLDER}/${id}-transcript-with-chapters.txt`;

  const checkFileExists = await $`test -s ${transcript_file}`.nothrow();

  if (checkFileExists.exitCode !== 0) {
    try {
      await $`python3 ${SCRIPT_DIR}/get_transcript.py https://www.youtube.com/watch?v=${id} > ${transcript_file}`;
    } catch (err) {
      // console.log(`Transcripts are disabled for video ID ${id}. Skipping this video.`);
      process.exit(1);
    }
  }

  const min_chapters=6
  const max_chapter_size=21
  await $`python3 ${SCRIPT_DIR}/add_chapters.py ${transcript_file} ${min_chapters} ${max_chapter_size}`.quiet();

  const num_chapters_output = await $`cat ${chapters_file} | grep -o "//.chapter-" | wc -l`.text();
  const num_chapters = parseInt(num_chapters_output.trim(), 10);
  // console.log(`Total Chapters: ${num_chapters}`);

  const sections = [];
  const section_size = 6;
  const overlap = 1;

  for (let i = 1; i <= num_chapters; i += section_size - overlap) {
    let from = i;
    let to = i + section_size - 1;
    
    if (to > num_chapters) {
      to = num_chapters;
    }
    
    if (to - from + 1 < 2) {
      break;
    }
    
    if (to + section_size - 1 > num_chapters) {
      to = num_chapters;
    }
    
    if (from <= num_chapters && to >= num_chapters) {
      sections.push(`${from}-${to}`);
      // console.log(`final ${from}-${to}`);
      break;
    }
    
    sections.push(`${from}-${to}`);
  }

  const final_markdown_file = `${DATA_FOLDER}/${id}-blogpost.md`;
  await $`rm -f ${final_markdown_file}`;
  // await $`> ${final_markdown_file}`;

  let previous_insight_response_file = 'empty';
  let previous_paragraph_response_file = 'empty';

  const total_sections = sections.length;

  // console.log(`Total Sections: ${total_sections}`);

	const skip_highlights = false;
	if (!skip_highlights) {
	  for (let section_index = 0; section_index < total_sections; section_index++) {
	    const section = sections[section_index];
	    const section_number = section_index + 1;

	    const [from, to] = section.split('-').map(Number);
	    const sanitized_section = section.replace(/\s+/g, '');

	    let transcript = "";
	    for (let j = from; j <= to; j++) {
	      transcript += `\nfile:${chapters_file}#chapter-${j}`;
	    }

	    // Generate QA prompt
	    const qa_prompt_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-qa-in.txt`;
	    const qa_response_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-qa-response.txt`;
	    await $`echo "|user|
Using direct, verbatim quotes from the provided transcript, create a concise series of question-answer pairs. Each answer must be an exact quote from the transcript, capturing the speaker original message without any paraphrasing or interpretation. Focus on extracting key insights, ensuring each quote stands alone coherently and maintains relevance when read sequentially.
|user|
${transcript}" > ${qa_prompt_file}`;
	    await $`python3 ${AI_DIR}/ai.py ${qa_prompt_file} --model=${model} --temperature=${temperature}`.quiet();

	    // Generate highlight prompt
	    const highlight_prompt_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-highlight-in.txt`;
	    const highlight_response_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-highlight-response.txt`;
			await $`echo "|system|
given a transcript of conversation please summarize it
|user|
${transcript}
|assistant|
file:${qa_response_file}
|user|
Try to prioritize direct quotes, stitching them together with triple dots, ensure as much quotes from original transcript incorporated, and do not use any comments or questions in your response other than quotes from original transcript. This is section ${section_number} of ${total_sections}." > ${highlight_prompt_file}`;
	    await $`python3 ${AI_DIR}/ai.py ${highlight_prompt_file} --model=${model} --temperature=${temperature}`.quiet();
	  }
	}

  // in first iteration we should avoid mentioning previous paragraph context
  let first_iteration = true;
  for (let i = 1; i <= num_chapters; i += section_size * 2 - overlap * 2) {
    let from = i;
    let to = i + section_size * 2 - overlap * 2;

    from = Number.parseInt(from.toString().replace(/\s+/g, ''));
    to = Number.parseInt(to.toString().replace(/\s+/g, ''));

    const paragraphPromptBase = 'transform given transcript into easy to read paragraphs formatted with markdown spoken coherently from the mouth of person in his first view, write from position of author only adding transition comments between sentences using cursive font wrapped with asteriks symbol';

    let paragraphPrompt;

    let single_highlight = false;
    if (to >= num_chapters) {
      single_highlight = true;
      to = num_chapters;
    } else if (to + section_size - overlap > num_chapters) {
      to = num_chapters;
    }

    const sanitized_section = `${from}-${to}`.replace(/\s+/g, '');

    if (first_iteration && single_highlight) {
      paragraphPrompt = `|user|
${paragraphPromptBase}
|user|
transcript of a new paragraph:
file:${DATA_FOLDER}/${id}-chapters-${from}-${to}-highlight-response.txt
`
    } else if (first_iteration && !single_highlight) {
      paragraphPrompt = `|user|
${paragraphPromptBase}
|user|
transcript of a new paragraph:
file:${DATA_FOLDER}/${id}-chapters-${from}-${to-section_size+overlap}-highlight-response.txt
file:${DATA_FOLDER}/${id}-chapters-${to-section_size+overlap}-${to}-highlight-response.txt`
    } else if (!first_iteration && single_highlight) {
      paragraphPrompt = `|user|
${paragraphPromptBase}, ensure its fits naturally as continuation of previous paragraph without repetition
|user|
previous paragraph:
file:${previous_paragraph_response_file}
|user|
transcript of a new paragraph:
file:${DATA_FOLDER}/${id}-chapters-${from}-${to}-highlight-response.txt
`
    } else {
      paragraphPrompt = `|user|
${paragraphPromptBase}
|user|
previous paragraph:
file:${previous_paragraph_response_file}
|user|
transcript of a new paragraph:
file:${DATA_FOLDER}/${id}-chapters-${from}-${from+section_size-overlap}-highlight-response.txt
file:${DATA_FOLDER}/${id}-chapters-${from+section_size-overlap}-${to}-highlight-response.txt`
    }

    const paragraph_prompt_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-paragraph-in.txt`;
    const paragraph_response_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-paragraph-response.txt`;

    await $`echo "${paragraphPrompt}" > ${paragraph_prompt_file}`;

    await $`python3 ${AI_DIR}/ai.py ${paragraph_prompt_file} --model=${model} --temperature=${temperature}`.quiet();
    // console.log(`Completed processing prompt ${paragraph_prompt_file}`);

    // Generate insight prompt
    const insight_prompt_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-insight-in.txt`;
    const insight_response_file = `${DATA_FOLDER}/${id}-chapters-${sanitized_section}-insight-response.txt`;

    const insightPromptBase = `|user|
extract single core insight expressed in a viral instagram-like way (yes can use emoji, but not hashtags) from a source paragraph
|user|
source paragraph:
file:${paragraph_response_file}`

    let insightPrompt;

    if (first_iteration) {
      insightPrompt = `${insightPromptBase}`;
    } else {
			insightPrompt = `${insightPromptBase}
|user|
previous insight:
file:${previous_insight_response_file}`;
    }

		await $`echo "${insightPrompt}" > ${insight_prompt_file}`;

    await $`python3 ${AI_DIR}/ai.py ${insight_prompt_file} --model=${model} --temperature=${temperature}`.quiet();
    // console.log(`Completed processing prompt ${insight_prompt_file}`);

    if (await $`test -f ${paragraph_response_file}`.nothrow() && await $`test -f ${insight_response_file}`.nothrow()) {
      const paragraph = await $`cat ${paragraph_response_file}`.text();
      const insight = (await $`cat ${insight_response_file}`.text()).trim().replace(/^"|"$/g, '');

      const temp_file = `${DATA_FOLDER}/temp-${id}-${from}-${to}.md`;

      await $`echo "## ${insight}" > ${temp_file}`;
      await $`echo "" >> ${temp_file}`;
      await $`echo "${paragraph}" >> ${temp_file}`;
      await $`echo "" >> ${temp_file}`;

      await $`cat ${temp_file} >> ${final_markdown_file}`;
      await $`rm -f ${temp_file}`;
    } else {
      // console.log(`Warning: Missing paragraph or insight file for section ${sanitized_section}`);
    }

    if (to >= num_chapters) {
      break;
    }

    previous_insight_response_file = insight_response_file;
    previous_paragraph_response_file = paragraph_response_file;

    first_iteration = false;
  }

  // Create post on Hashnode and copy the file
  await $`HASHNODE_DOMAIN="guryeah.hashnode.dev" python3 ${SCRIPT_DIR}/create_post.py ${final_markdown_file}`.quiet();
  await $`cp ${DATA_FOLDER}/${id}-hashnode.md ${process.env.HOME}/Documents/hashnode-july24`;

  console.log(`${DATA_FOLDER}/${id}-hashnode.md`)

  // console.log(`Post created for video ID ${id}`);
}

await main();
