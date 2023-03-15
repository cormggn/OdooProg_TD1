{
    "name": "Gestion des étudiants",
    "version": "2.0",
    "category": "Generic Modules/Others",
    "description": """Test création module gestion des étudiants Odoo v14""",
    "author": "goganc",
    "depends": ["base"],
    "data": [
        "data/students_training_data.xml",
        "data/students_student_data.xml",
        "data/students_mark_data.xml",
        "views/students_views.xml",
        "views/students_continuous_views.xml",
        "views/trainings_views.xml",
        "views/notes_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}