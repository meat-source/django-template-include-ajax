# django-template-include-ajax

Purpose: django Tag, similar to the standard `{% include 'template.html' %}` for deferred template loading via
ajax.The template is wrapped in `<div>` Supports both internal and external scripts in the template (via
the html tag `<sсript>`). Has an optional condition on
the minimum and maximum screen width for loading the template. They are used for separating mobile,
desktop and tablet versions of the template). It also has an optional `delWrap`argument,
which removes the wrapper around the content. Disabled by default.(when enabled, it does not allow external scripts to 
load).
```
{% include_ajax 'example_not_wrap.html' delWrap='True' %}
```

It doesn't make sense to wrap this code in a separate django app. It is more appropriate to implement this tag
directly to your project.

does not have any dependencies

## Getting Started
After loading in the template tag `{% load template_include_ajax %}`
uploading the template via ajax, where example.html template name
``
{% include_ajax 'example.html' %}
``
if the template is in a subfolder, specify it
``
{% include_ajax 'folder/example.html' %}
``
you can also specify additional parameters minWidth and maxWidth, beyond which ajax will not be triggered.
```
{% include_ajax 'example_only_tablet.html' minWidth='576' maxWidth='1025' %}
```
There is also an additional delWrap parameter that removes the wrapper around the content.Disabled by default.
(when enabled, it does not allow external scripts to load).

### Installing
In your app, create a templatetags folder with the include_ajax file. Then in the project urls we add
``
path('include-ajax/<template>', include_ajax),
``

enabling processing in views

``
def include_ajax(request, template):
template = template.replace('&', '/') # for templates that are nested in a folder
try:
return render(request, template)
except TemplateDoesNotExist:
return HttpResponse(status=404)
``

loading the tag in the template
``
{% load template_include_ajax %}
``
Everything. Use.
## Importantly:
1) working scripts are self-deleted after loading and execution ! (you should keep this in mind when checking and debugging)
2) external scripts are written to the end of the block (i.e. after the data)
3) your template will be wrapped in `<div>` you can remove the wrapper by using the additional delWrap parameter, but
external scripts (for example, Yandex map) will not have time to fire.


## Running tests

You can test it by downloading the demo and connecting it as a regular django project


## Contributing

Please send suggestions, errors in the work and comments to the email address ukolovsl88@gmail.com

## Versioning

It was tested on django 2.1.10 - 2.2.10, but it will probably work in earlier versions as well.

## Author

**Slava Ukolov**  - [github.com/meat-source](https://github.com/meat-source)

## License

This project is licensed under the MIT license - [LICENSE.md](LICENSE.md)