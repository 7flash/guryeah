Welcome to the GurYeaH documentation! This project contains scripts and workflows to convert YouTube videos, specifically podcasts, into structured and readable Hashnode blog posts. The method has proven to save significant time by summarizing and formatting content that's otherwise lengthy to listen to. Below you will find detailed instructions on how to set up, use, and customize this project to fit your needs.

## Table of Contents
1. [Introduction](docs/introduction.md)
2. [Setup and Dependencies](docs/setup.md)
3. [Workflow](docs/workflow.md)
4. [Configuration](docs/configuration.md)
5. [Running the Scripts](docs/running_scripts.md)
6. [Customizing](docs/customizing.md)
7. [Contributing](docs/contributing.md)

---

## Introduction

GurYeaH aims to streamline the process of converting YouTube podcasts into blog posts by focusing on key quotes and moments from the conversations. It splits the transcript into manageable parts, extracts meaningful quotes, and formats them into a readable blog post. This method can save a lot of time and effort for those who prefer reading over listening.

To read more about the purpose and background of this project, please refer to [Introduction](docs/introduction.md).

## Setup and Dependencies

Before you can start using the scripts, you'll need to set up your environment and install necessary dependencies. This project relies on several tools and libraries including YouTube API, GPT-3, and PocketTube.

To get started, follow the guide in [Setup and Dependencies](docs/setup.md).

## Workflow

Understanding the workflow is crucial for effectively using and customizing the scripts. The workflow includes these steps:
1. Extracting the transcript from YouTube.
2. Splitting the transcript into manageable sections.
3. Extracting key quotes and generating questions.
4. Summarizing and formatting the text.
5. Generating a title and merging all sections.
6. Formatting the final output into a Hashnode-compatible markdown.

For a detailed explanation, visit [Workflow](docs/workflow.md).

## Configuration

The script is highly configurable. You can adjust settings to match your preferences, such as the length of sections, overlap between sections, and more. Configuration is handled via `config.txt`.

For details on how to set up and use the configuration file, see [Configuration](docs/configuration.md).

## Running the Scripts

Once everything is set up, you can run the scripts to process your playlists. Typically, this involves running a shell script with specific parameters such as the range of videos to process.

Step-by-step instructions can be found in [Running the Scripts](docs/running_scripts.md).

## Customizing

You might want to tweak how the scripts work, such as adjusting prompts for GPT-3, changing the output format, or adding new features. This section provides tips and examples for customization.

Learn more in [Customizing](docs/customizing.md).

## Contributing

This project is open-source and welcomes contributions. Whether you want to report an issue, suggest a new feature, or submit a pull request, please see [Contributing](docs/contributing.md) for guidelines.

---

Remember to always manually review the drafts generated by the script to ensure quality and accuracy before publishing them on Hashnode.

Happy blogging!
