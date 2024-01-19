from django.shortcuts import render

db = {
    "reactors": [
        {
            "id": 1,
            "name": "ЭГП-6",
            "coolant": "вода",
            "fuel": "диоксид урана",
            "thermal_power": "80",
            "electrical_power": "20"
        },
        {
            "id": 2,
            "name": "АМБ-200",
            "coolant": "вода",
            "fuel": "двуокись урана",
            "thermal_power": "65",
            "electrical_power": "12"
        },
        {
            "id": 3,
            "name": "РБМК-1000",
            "coolant": "вода",
            "fuel": "диоксид урана",
            "thermal_power": "50",
            "electrical_power": "11"
        },
        {
            "id": 4,
            "name": "ВВЭР-1000",
            "coolant": "вода",
            "fuel": "диоксид урана",
            "thermal_power": "30",
            "electrical_power": "10"
        }
    ],
}


def index(request):
    query = request.GET.get("reactor", "")

    context = {
        "reactors": searchReactors(query),
        "query": query,
    }

    return render(request, "home_page.html", context)


def reactorPage(request, reactor_id):
    context = {
        "reactor": getReactor(reactor_id)
    }

    return render(request, "reactor_page.html", context)


def searchReactors(reactor_name=""):
    res = []

    for reactor in db["reactors"]:
        if reactor_name.lower() in reactor["name"].lower():
            res.append(reactor)

    return res


def getReactor(reactor_id):
    for reactor in db["reactors"]:
        if reactor["id"] == reactor_id:
            return reactor