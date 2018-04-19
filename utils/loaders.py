from jinja2 import Environment, FileSystemLoader


def render_from_template(
        directory, template_name, custom_filters=None,
        trim_blocks=True, lstrip_blocks=True, **kwargs
        ):
    """
    Render template with customer filters
    """
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader, trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)

    if custom_filters is not None:
        for custom_filter in custom_filters:
            env.filters[custom_filter.__name__] = custom_filter

    template = env.get_template(template_name)
    return template.render(**kwargs)
