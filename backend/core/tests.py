from django.test import TestCase

from django.urls import reverse


class PublicPageTests(TestCase):
    def test_public_pages_render(self):
        for page_name in ("home", "about", "contact", "workflow"):
            response = self.client.get(reverse(f"core:{page_name}"))
            self.assertEqual(response.status_code, 200)

    def test_workflow_stages_are_rendered_from_view_context(self):
        response = self.client.get(reverse("core:workflow"))

        self.assertContains(response, "Request submitted")
        self.assertContains(response, "Request triaged")
        self.assertContains(response, "Technician assigned")
        self.assertContains(response, "Request resolved")
        self.assertEqual(response.context["stages"], [
            "Request submitted",
            "Request triaged",
            "Technician assigned",
            "Request resolved",
        ])

    def test_active_navigation_link(self):
        for page_name, label in (
            ("home", "Home"),
            ("about", "About"),
            ("contact", "Contact"),
        ):
            response = self.client.get(reverse(f"core:{page_name}"))

            self.assertContains(
                response,
                f'<a href="{reverse(f"core:{page_name}")}" aria-current="page">{label}</a>',
                html=True,
            )

    def test_custom_404_template(self):
        with self.settings(DEBUG=False):
            response = self.client.get("/does-not-exist/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page not found", status_code=404)
