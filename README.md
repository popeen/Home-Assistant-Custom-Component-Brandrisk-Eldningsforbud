## Home Assistant Custom Component: Brandrisk & Eldningsförbud

[![GitHub Release][releases-shield]][releases]
[![downloads-shield]][release-link]
![Project Stage][project-stage-shield]
[![issues-shield]](issues)
[![License][license-shield]](LICENSE.md)
[![hacs_badge][hacs-shield]][hacs]
[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

This custom component will give you two sensors for MSBs [Brandrisk Ute](https://www.msb.se/sv/om-msb/informationskanaler/appar/brandrisk-ute/).
The sensors are:
* Risk of fire
* Fire Prohibition

The risk sensor returns a risk index value. It has a text description of the value as an attribute but if you want to see a list of all the avalable values you can do so at https://api.msb.se/brandrisk/v2/RiskLevels/sv. This could be useful when writing automations.

I have started the process of getting this repo included in the default HACS library but for now you have to add it to your HACS using [these instructions](https://hacs.xyz/docs/faq/custom_repositories/)

After installing the integration using HACS and restarting your server you simply add it by clicking the button below or by going to Devices & Services and adding it from there.

[![add-integration-shield]][add-integration]


[downloads-shield]: https://img.shields.io/github/downloads/popeen/Home-Assistant-Custom-Component-Brandrisk-Ute/total
[release-link]: https://github.com/popeen/Home-Assistant-Custom-Component-Brandrisk-Ute/releases
[releases-shield]: https://img.shields.io/github/release/popeen/Home-Assistant-Custom-Component-Brandrisk-Ute.svg
[releases]: https://github.com/popeen/Home-Assistant-Custom-Component-Brandrisk-Eldningsforbud/releases
[project-stage-shield]: https://img.shields.io/badge/project%20stage-ready%20for%20use-green.svg
[issues-shield]: https://img.shields.io/github/issues-raw/popeen/Home-Assistant-Custom-Component-Brandrisk-Eldningsforbud.svg
[license-shield]: https://img.shields.io/github/license/popeen/Home-Assistant-Custom-Component-Brandrisk-Eldningsforbud.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[hacs]: https://github.com/custom-components/hacs
[buymeacoffee-shield]: https://img.shields.io/badge/donation-Buy%20me%20a%20coffee-orange
[buymeacoffee]: https://www.buymeacoffee.com/popeen
[add-integration-shield]: https://my.home-assistant.io/badges/config_flow_start.svg
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start/?domain=brandriskute
