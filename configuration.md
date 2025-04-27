### configuration.md:

```markdown
---
layout: default
title: Configuration Options
nav_order: 3
---

# Configuration Options

## Configuration Methods

You can provide configuration parameters through:
- `rs_automation/pytest.ini`
- `rs_automation/.default_env` (for default environment variables)
- `rs_automation/.env` (for personal environment variables, git-ignored)
- Pytest command line options
- Environment variables

> It's allowed to have the same variables in both `.env` and `.default_env`. In this case, the value in `.env` will take precedence.
> Therefore, it's recommended to leave `.default_env` untouched and edit only the `.env` file.

## Parameters Reference

| Parameter | Required | Description | Default |
|:---|:---|:---|:---|
{% for param_name in site.data.parameters %}
{% assign param = site.data.parameters[param_name] %}
| {{ param_name }} | {{ param.required | default: "False" | capitalize }} | {{ param.description | default: "" | strip }} | {% if param.default == nil %}None{% elsif param.default == "" %}Empty string{% elsif param.default == false %}False{% elsif param.default == true %}True{% else %}`{{ param.default }}`{% endif %} |
{% endfor %}

## AWS Credentials

### Working with one AWS profile
[AWS profile login and credentials](https://redislabs.atlassian.net/wiki/spaces/RED/pages/3372122127/Non+Production+Cloud+Accounts+Access#Console-Access)

Set these values as environment variables in `.env`:

| Value | Required | Description | Default |
|:---|:---|:---|:---|
| AWS_ACCESS_KEY_ID | Yes if no profile configured | Access key used to authenticate with AWS services | |
| AWS_SECRET_ACCESS_KEY | Yes if no profile configured | Secret access key used to authenticate with AWS services | |
| AWS_SESSION_TOKEN | Yes if no profile configured | Temporary token | |

### Working with multiple AWS accounts
The steps to configure AWS profile: [AWS profile](https://redislabs.atlassian.net/wiki/spaces/RED/pages/3372122127/Non+Production+Cloud+Accounts+Access#Working-with-multiple-AWS-accounts-and-Profile-at-the-same-time)
- Add `AWS_PROFILE = "<YOUR AWS PROFILE>"` to your `.env` file