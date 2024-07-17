function sendCity(event) {
    if (event.key == 'Enter'){
        let search_value = document.getElementById('search-input').value

        fetch('/changeCity', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({city: search_value})
        })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    location.href = ''
                }else {
                    alert('Ошибка. Попробуйте снова')
                    document.getElementById('search-input').value = ''
                }
            })
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let mainContent = document.getElementById('body-main-content')
    let searchHelp = document.getElementById('search-help')
    let isSearchOpen = false

    document.getElementById('search-input').addEventListener('focus', function () {
        searchHelp.classList.remove('hide')
        isSearchOpen = true
        document.querySelector('.search').style.opacity = 1
        mainContent.style.opacity = 0.5
        document.addEventListener('keydown', sendCity)
    })
    document.getElementById('search-input').addEventListener('blur', function () {
        mainContent.style.opacity = 1
        isSearchOpen = false
        searchHelp.classList.add('hide')
        document.removeEventListener('keydown', sendCity)
    })

    let btns = document.querySelectorAll('.button')
    btns.forEach(btn => {
        btn.addEventListener('click', function () {
            location.href = `/?time=${btn.id.split('-')[1]}`
        })
    })
    
    let search_help_city_btns = document.querySelectorAll('.search-help-city')
    search_help_city_btns.forEach(btn => {
        btn.addEventListener('click', function () {
            console.log(1)
            searchHelp.value = btn.id
            var evt = new KeyboardEvent('keydown', {'keyCode':13, 'which':65});
            document.dispatchEvent(evt);
        })
    })


    document.getElementById('search-help').addEventListener('click',function(event){
        if (isSearchOpen){
            searchHelp.focus()
        }
    })

})