
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO *Removed this since we don't have a logo yet*-->
<br />
<div align="center">
<h3 align="center">RAAM</h3>

  <p align="center">
    A small project to implement Giordano's Ranked Asset Allocation Model and compare it against other portfolio allocation methods.
    <!--
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
    -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The goal of this project is to explore automated methods for allocating a stock/ETF/crypto portfolio, starting with implementing [Giordano's 2018 Ranked Asset Allocation Model](https://tanassociation.org/wp-content/uploads/2018/05/2018_dowaward-giordano.pdf)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

**Will be fleshed out over time as project grows**
### Prerequisites

 - Python 3.8.5
 - yahooquery 2.2.15
 - pandas 1.3.3

### Installation
**This is an example, this is now how to run our project. This needs updated as we flesh the project out.**
1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The main usage for now is interaction through discord via bot commands, but this
project can be run directly on your local machine. Our goal is to create multiple
interaction avenues eventually via: commandline, discord bot, and a web interface.

Currently, you can launch the bot by navigating to the discord_bot and running bot.py. When connected to the server you can run:
`!run-raam` to see how RAAM allocates the current top ten NASDAQ assets.

You can specify your own list of assets with `!run-raam assets=ASSET1,ASSET2,ASSET3...` where `ASSET1,ASSET2,ASSET3,` are the ticker abbreviations for each asset (such as `GOOG`, `AAPL`, `SPY`).
More documentation exists for how to run the bot on the server's bot-documentation channel.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
**---TDB---**
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions must be made via an appropriate branching strategy and then reviewed by one of the project leads. Simply follow these
steps to contribute!

1. Clone the repository (`git clone https://github.com/wfraher/RAAM-python.git`)
2. Create your Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit your Changes (`git commit -m 'Add some amazing-feature'`)
4. Push to the Branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Be sure you are using the pattern [type of change]/[description of change]
accepted types of change include:
- feature
- bugfix
- hotfix

Examples of branch names include:
- feature/add-new-commandline-args
- bugfix/could-not-load-cvs-files

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []() Fill these out as project progresses
* []() For now, these are here for template

<p align="right">(<a href="#readme-top">back to top</a>)</p>