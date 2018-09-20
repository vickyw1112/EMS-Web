<script charset="utf-8">
    var data = {};

    $(window).on('load', function(){
        for(let ele of document.querySelectorAll("form input[name], form textarea[name]")){
            if(ele.type == "submit" || ele.type == 'button' || ele.type == 'hidden')
                continue;
            ele.setAttribute('v-model', ele.name);
        }

        {% if form %}
        data = {{form | safe}};
        {% else %}
        for(let ele of document.querySelectorAll("form input[name], form textarea[name]")){
            data[ele.name] = '';
        }
        {% endif %}

        var vm = new Vue({
            el: '#app',
            data: data
        });
    })
</script>
