from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(name='include_ajax')
def include_ajax(template, minWidth='undefined', maxWidth='undefined', delWrap =False):
    """
    Назначение: django-Тег для отложенной загрузки шаблона через ajax. Поддерживает, как внутренние так и внешние
    скрипты (через html-тег <sсript>). Имеет необязательное условие на минимальную и максимальную ширину экрана, при
    котором загружается шаблон. Также имеет необязательный аргумент delWrap, который убирает обертку вокруг содержимого.
    По умолчанию отключен.(ПРИ ВКЛЮЧЕНИИ НЕ ДАЕТ ЗАГРУЗИТСЯ ВНЕШНИМ СКРИПТАМ).

    тестировалось на django 2.1.10
    Создатель Вячеслав Уколов. вопросы и предложения по почте - (ukolovsl88@gmail.com)


    ВНИМАНИЕ: рабочие скрипты после загрузки и исполнения самоудаляются !
    ВНИМАНИЕ №2: внешние скрипты записываются в конец блока (т.е после данных)
    ВНИМАНИЕ №3: ваш шаблон будет обернут в <div> вы можете убрать обертку раскомментировав строку ниже, но при этом не
    будут успевать срабатывать внешние скрипты (допустим яндекс карта)
    смысл такой: на вход приходит имя шаблона. Допольнительно максимальная и/или минимальная ширина экрана браузера
    на выходе <div> с именем шаблона и солью + два скрипта один это ajax (загружает данные) и
    onload вешает обработчик событий на конец загрузки страницы с запуском ajax
    данная функция должна использоваться вместе вьъюхой и урл
    вьюха:
        def include_ajax(request, template):
            template = template.replace('&', '/')  # для шаблонов вложенных в папку
            try:
                return render(request, template)
            except TemplateDoesNotExist:
                return HttpResponse(status=404)
    урл (в проекте!):
        path('include-ajax/<template>', include_ajax),
    """
    # Функция Include - Ajax - запроса(непосредственно запрос)
    import random
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'm', 'i', 'k', 'l', 'o', 'p', 'r', 's', 't', 'n']
    # соль
    sol = ''.join(map(str, random.sample(a, 5)))
    # удаляет  скрипты после работы
    del_garbage = "document.getElementById('ajax_" + sol + "').remove();document.getElementById('onload_" + sol \
                  + "').remove();"
    # Если есть аргументы ширины сравниваем с окном браузера и выходим если не подходит
    if minWidth != 'undefined' or maxWidth != 'undefined':
        mobile_or_destktop = "if (screen.width < " + minWidth + " || screen.width > " \
                             + maxWidth + "){" + del_garbage + " return}"

    else:
        mobile_or_destktop = ''
    # выполняет скрипты в теле ajax
    execute_script = """function executeScripts (obj){ 
        var head = document.getElementsByTagName('head')[0];
        var scripts = obj.getElementsByTagName('script');
        
        for(var i = 0; i < scripts.length; i++){
            let str = scripts[i].outerHTML;
            let newSrc =  str.match(/data-script-src=['"][^'"]*[^"]/gi);
            if(newSrc != null){
                newSrc = newSrc[0].replace('data-script-src=','');
                newSrc = newSrc.replace(/['"]/g,'');
            }
            eval(scripts[i].innerHTML);
            
            if(newSrc != null){
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = newSrc;
                obj.appendChild(script);
                //scripts[i].src = '';
            }
        }
    }"""
    # Сборка и вставка скриптов после пирнятия ответа серверра
    # (block.outerHTML=block.innerHTML убирает обертку, но при этом не успевают сработать внешние скрипты)
    if delWrap:
        post_send = execute_script + "executeScripts(block);" + del_garbage + "block.outerHTML= block.innerHTML"
    else:
        post_send = execute_script + "executeScripts(block);" + del_garbage  # + "block.outerHTML= block.innerHTML"

    # непосредственно сам ajax
    include_ajax = """<script id='ajax_""" + sol + """'>
    function SendAjax_""" + sol + """(){
        """ + mobile_or_destktop + """
        var url =document.location.protocol +'//'+ document.location.host
            + '/include-ajax/""" + template.replace('/', '&') + """';
        var request = new XMLHttpRequest();
        request.open('GET', url);
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        request.addEventListener('readystatechange', () => {
            if (request.status === 200 && request.readyState  === XMLHttpRequest.DONE) {
                var block = document.getElementById('""" + template + """');
                function replace_src(str){return str.replace(/src/g,'data-script-src')};
                block.innerHTML = request.responseText.replace(/<script.*<\/script>/g, replace_src);
                // console.log(block.innerHTML)
                console.log( 'include-ajax: подгружен template - ' + '""" + template + """');
                """ + post_send + """
            }
            if (request.status != 200){
                console.error( 'include-ajax: подгрузка шаблона не удалась - ' + '""" + template + """ --- ' 
                    + request.status + ' --- ' + request.statusText)
            };
        });
        request.send();
    }
    </script>"""
    # вешаем событие
    onload_body = """<script id='onload_""" + sol + """'>
        function addEvent_""" + sol + """(elem, type, handler){
            if(elem.addEventListener){    elem.addEventListener(type, handler, false);}
            else {    elem.attachEvent('on'+type, handler);}
            return false;
        };
        addEvent_""" + sol + """(window, 'load', SendAjax_""" + sol + """);
    </script>"""
    # обертка для будущего блока
    block = "<div data-defer-template id='" + template + "'></div>"
    response = block + include_ajax + onload_body

    return mark_safe(response)
