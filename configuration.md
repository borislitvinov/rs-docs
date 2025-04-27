---
layout: default
title: "Configuration Options"
nav_order: 6
---

# Configuration Options

| Parameter | Required | Description | Default |
|:---|:---|:---|:---|
{% raw %}
{% for param_name in site.data.parameters %}
{% assign param = site.data.parameters[param_name] %}
| {{ param_name }} | {{ param.required | capitalize }} | {{ param.description | strip }} | {% if param.default %}{{ param.default }}{% else %}None{% endif %} |
{% endfor %}
{% endraw %}