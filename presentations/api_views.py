from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Presentation, Status
from django.views.decorators.http import require_http_methods
import json


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


class PresentationEncoder(ModelEncoder):
    properties = [
        "presenter_name",
        "title",
    ]


@require_http_methods(["GET", "DELETE", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation, encoder=PresentationDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        Presentation.objects.filter(id=id).update(**content)

        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(
            conference_id=conference_id
        )
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    else:
        content = json.loads(request.body)
        try:
            content["conference_id"] = conference_id
            presentation = Presentation.create(**content)
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "conference_id invalid"}, status=400
            )
        return JsonResponse(
            presentation, encoder=PresentationDetailEncoder, safe=False
        )
    """
    Lists the presentation titles and the link to the
    presentation for the specified conference id.

    Returns a dictionary with a single key "presentations"
    which is a list of presentation titles and URLS. Each
    entry in the list is a dictionary that contains the
    title of the presentation, the name of its status, and
    the link to the presentation's information.

    {
        "presentations": [
            {
                "title": presentation's title,
                "status": presentation's status name
                "href": URL to the presentation,
            },
            ...
        ]
    }
    """
    # presentations = [
    #     {
    #         "title": p.title,
    #         "status": p.status.name,
    #         "href": p.get_api_url(),
    #     }
    #     for p in Presentation.objects.filter(conference=conference_id)
    # ]
    # return JsonResponse({"presentations": presentations})

    # def api_show_presentation(request, id):
    """
    Returns the details for the Presentation model specified
    by the id parameter.

    This should return a dictionary with the presenter's name,
    their company name, the presenter's email, the title of
    the presentation, the synopsis of the presentation, when
    the presentation record was created, its status name, and
    a dictionary that has the conference name and its URL

    {
        "presenter_name": the name of the presenter,
        "company_name": the name of the presenter's company,
        "presenter_email": the email address of the presenter,
        "title": the title of the presentation,
        "synopsis": the synopsis for the presentation,
        "created": the date/time when the record was created,
        "status": the name of the status for the presentation,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    # presentation = Presentation.objects.get(id=id)

    # return JsonResponse(presentation, PresentationEncoder, safe=False)
    # return JsonResponse(
    #     {
    #         "presenter_name": presentation.presenter_name,
    #         "company_name": presentation.company_name,
    #         "presenter_email": presentation.presenter_email,
    #         "title": presentation.title,
    #         "synopsis": presentation.synopsis,
    #         "created": presentation.created,
    #         "status": presentation.status.name,
    #         "conference": {
    #             "name": presentation.conference.name,
    #             "href": presentation.conference.get_api_url(),
    #         },
    #     },
    # )
