from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
	"platform_name": "VUA ServiceDesk ",
	"headline": "Report and track maintenace requests",
	"active_requests": 0,
   }

    return render(request, "core/home.html", context)

def about(request): 
    project_roles =  [ "Requester",
                      "Coordinator",
                      "Technician",
                     "Administrator", ] 


    return render(request, "core/about.html", {"project_roles": project_roles}, )

def contact(request):
    context = {
        "department_name": "Service Desk Support",
        "office_hours": "Monday to Friday, 08:00 to 17:00",
        "email": "servicedesk@example.com",
    }

    return render(request, "core/contact.html", context)


def workflow(request):
    stages = [
        "Request submitted",
        "Request triaged",
        "Technician assigned",
        "Request resolved",
    ]

    return render(request, "core/workflow.html", {"stages": stages})