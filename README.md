# Dota 2 Overlay

> Disclaimer: This project was created with the assistance of artificial intelligence.
> While the code has been designed to function properly,
> it may require additional testing and refinement for production use.

## Overview

Dota 2 Hero Counter Overlay is a desktop application that provides real-time hero counter information during Dota 2 matches. The application features an always-on-top overlay that displays hero counters, win rates, and hero images, helping players make informed decisions during hero selection.

## Features

  *  Real-time Hero Data: Fetches counter information directly from Dotabuff

  *  Overlay Mode: Always-on-top transparent overlay that can be positioned anywhere on screen

  *  Hero Images: Displays hero images using Steam CDN

  *  Customizable Appearance: Multiple theme options and customizable overlay size/opacity

  *  Secure API Key Storage: Encrypted storage for API keys

  *  Standalone Overlay: Independent overlay window with hero selection and data fetching

## Installation
### Prerequisites

  *  Python 3.7+

  *  Firefox browser (for Selenium webdriver)

  *  Geckodriver (included with Selenium or can be installed separately)

#### Steps

1. Clone the repository:

```
git clone https://github.com/yourusername/dota2-hero-counter-overlay.git 
cd dota2-hero-counter-overlay
```

2. Install required dependencies:

```
pip install -r requirements.txt 
```

3. Run the application:

```
python main.py 
```

## Usage

   1. Main Window:

      *  Select a hero from the dropdown menu

      *  Click "Fetch Data" to retrieve counter information

      *  Toggle the overlay using the checkbox

   2. Overlay Window:

      *  Drag to reposition the overlay anywhere on screen

      *  Select heroes directly from the overlay's dropdown

      *  Click "Fetch" to update the overlay with new hero data

   3. Settings:

      *  Access settings from the main window

      *  Configure API keys (Steam API key for hero images)

      *  Customize appearance (themes, opacity, overlay size)

## Configuration
### API Keys

### The application requires a Steam API key to fetch hero images:

   * Obtain a Steam API key from Steam Web API

   * Open the settings dialog in the application

   * Enter your API key in the "Steam API Key" field

## Themes

Choose from multiple themes:

   * Dark (default)

   * Light

   * Custom (with color picker)


## Dependencies

  *  PyQt5 - GUI framework

  *  Selenium - Web scraping

  *  BeautifulSoup4 - HTML parsing

  *  Requests - HTTP requests

  *  Cryptography - Secure data encryption

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

   1. Fork the project

   2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

   3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

   4. Push to the branch (`git push origin feature/AmazingFeature`)

   5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
Disclaimer

This application is not affiliated with or endorsed by Valve Corporation, Dota 2, or Dotabuff. It is a fan-made tool designed to help players access publicly available information more conveniently.
Support

If you encounter any issues or have questions, please open an issue on GitHub.







