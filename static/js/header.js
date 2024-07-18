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
                    alert('Ошибка. Город не найден')
                    document.getElementById('search-input').value = ''
                    document.getElementById('search-input').blur()
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
        searchHelp.style.opacity = 1
        document.querySelector('.search').style.opacity = 1
        mainContent.style.opacity = 0.5
        document.addEventListener('keydown', sendCity)
    })
    document.getElementById('search-input').addEventListener('blur', function () {
        searchHelp.style.opacity = 0
        mainContent.style.opacity = 1
        isSearchOpen = false
        document.removeEventListener('keydown', sendCity)
        setTimeout(function () {
            searchHelp.classList.add('hide')
        }, 100)
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
            let city = btn.innerText
            window.location.href = '/?city=' + city
        })
    })


    document.getElementById('search-help').addEventListener('click',function(event){
        if (isSearchOpen){
            searchHelp.focus()
        }
    })

})