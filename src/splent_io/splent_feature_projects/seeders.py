import re

from splent_framework.seeders.BaseSeeder import BaseSeeder

from splent_io.splent_feature_projects.models import Project


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _norm_status(raw: str) -> str:
    return "active" if raw.strip().lower() == "active" else "past"


_PROJECTS = [
    {
        "acronym": "SENSOLIVE",
        "title": "Deficit irrigation system in olive groves using dendrometers and intelligent digital twins",
        "summary": "Deficit irrigation system in olive groves using dendrometers and intelligent digital twins.",
        "funding": "Otros Proyectos Junta Andalucia - Junta de Andalucia: Consejeria de Universidad, Investigacion e Innovacion",
        "status": "Active",
        "link": "",
    },
    {
        "acronym": "ENFOCA",
        "title": "Ensamblado de Nodos mediante Federacion Optimizada de Conocimiento Autocodificado en Patologia Digital",
        "summary": "Knowledge-federation framework for digital pathology, assembling nodes via optimized federation of autocoded knowledge.",
        "funding": "Plan Estatal 2021-2023 - Proyectos Investigacion Orientada - Ministerio de Ciencia, Innovacion y Universidades",
        "status": "Active",
        "link": "",
    },
    {
        "acronym": "DATA-PL",
        "title": "Data-Intensive Software Product Lines",
        "summary": "Data-Intensive Software Product Lines.",
        "funding": "Proyectos de generacion de conocimiento 2022 - Ministerio de Ciencia e Innovacion",
        "status": "Active",
        "link": "",
    },
    {
        "acronym": "METAMORFOSIS",
        "title": "Digital Transformation Framework through Customised Software on Data Management, Business Processes and Security Governance",
        "summary": "Digital Transformation Framework through Customised Software on Data Management, Business Processes and Security Governance.",
        "funding": "Andalusia ERDF R+D+i projects - Consejeria de Economia, Conocimiento, Empresas y Universidad (01/01/2022 - 31/05/2023)",
        "status": "Past",
        "link": "",
    },
    {
        "acronym": "COPERNICA",
        "title": "Business Process Collaboration For Good Governance of Shared Services and Data",
        "summary": "Business Process Collaboration For Good Governance of Shared Services and Data.",
        "funding": "PAIDI 2020: R&D&I Projects - Consejeria de Economia, Conocimiento, Empresas y Universidad",
        "status": "Past",
        "link": "",
    },
    {
        "acronym": "TASOVA PLUS",
        "title": "Red en nuevas Tendencias en Arquitectura Software y Variabilidad",
        "summary": "Research network on new trends in software architecture and variability.",
        "funding": "Conv. 2022 Redes de Investigacion - Ministerio de Ciencia e Innovacion",
        "status": "Past",
        "link": "",
    },
    {
        "acronym": "MIDAS",
        "title": "Monitorizacion Inteligente y Digitalizacion Avanzada de Servicios de Marketing",
        "summary": "Intelligent monitoring and advanced digitalization of marketing services.",
        "funding": "Contrato 68/83 - Consultoria Informatica Acofi",
        "status": "Past",
        "link": "",
    },
    {
        "acronym": "AQUAIA",
        "title": "Sistema de programacion de riego deficitario para cultivos (Grupo Operativo)",
        "summary": "Operational-group system for scheduling deficit irrigation in crops.",
        "funding": "Otros Proyectos Junta Andalucia - Junta de Andalucia",
        "status": "Past",
        "link": "",
    },
    {
        "acronym": "PLANT",
        "title": "Por resolver (to be resolved)",
        "summary": "Listed on the projects page under 'TO BE RESOLVED' / 'Por resolver'; details not yet published.",
        "funding": "",
        "status": "To be resolved",
        "link": "",
    },
]


class ProjectsSeeder(BaseSeeder):
    def run(self):
        data = []
        for order, item in enumerate(_PROJECTS, start=1):
            slug = _slugify(item["acronym"] or item["title"])
            data.append(
                Project(
                    acronym=item["acronym"],
                    title=item["title"],
                    slug=slug,
                    summary=item["summary"],
                    description=item["summary"],
                    funding=item["funding"],
                    status=_norm_status(item["status"]),
                    link=item["link"],
                    order=order,
                    published=True,
                )
            )
        self.seed(data)
