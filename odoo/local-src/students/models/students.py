from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class StudentsTraining(models.Model):
    _name = "students.training"
    _description = "Training table"
    _rec_name = "code"
    code = fields.Char(string="Training code", size=4, required=True)
    name = fields.Char(string="Training name", size=100, required=True)
    student_ids = fields.One2many(
        string="Training students",
        comodel_name="students.student",
        inverse_name="training_id",
    )
#    @api.constrains('code')
#    def _check_training_code(self):
#       for record in self:
#            if self.env['students.training'].search([('code', '=', record.code)]):
#                raise ValidationError(_("Training code already exists"))

class StudentsStudent(models.Model):
    _name = "students.student"
    _description = "Student table"
    # _rec_name = "number"
    number = fields.Char("Student number", size=11, required=True)
    firstname = fields.Char("Student firstname", size=64, required=True)
    lastname = fields.Char("Student lastname", size=64, required=True)
    nationality = fields.Many2one(
        string="Nationality",
        comodel_name="res.country",
        ondelete="set null",
    )
    training_id = fields.Many2one(
        string="Training",
        comodel_name="students.training",
        ondelete="cascade",
    )
    mark_ids = fields.One2many(
        string="Marks",
        comodel_name="students.mark",
        inverse_name="student_id"
    )
    gpa = fields.Float(
        string="Grade point average",
        compute="_compute_gpa",
    )
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s %s' % (record.firstname, record.lastname)))
        return result
    @api.onchange("mark_ids")
    def _compute_gpa(self):
        for record in self:
            average = 0
            if record.mark_ids:
                total_coeff = sum(int(m.coefficient) for m in record.mark_ids)
                total_mark = sum(m.weighted_mark for m in record.mark_ids)
                if total_coeff != 0:
                    average = total_mark / total_coeff
            record.gpa = average

class StudentsMarks(models.Model):
    _name = "students.mark"
    _description = "Marks table"
    subject = fields.Char("Subject", size=64, required=True)
    coefficient = fields.Selection(
        string="Coefficient",
        selection=[('1', "1"), ('2', "2"), ('3', "3"), ('5', "5")],
        index=True,
        default="1",
        help="Select a coefficient in the list",
        required=True,
    )
    mark = fields.Float("Mark", required=True)
    student_id = fields.Many2one(
        string="Students Marks",
        comodel_name="students.student",
        ondelete="cascade",
        required=True,
    )
    weighted_mark = fields.Float(
        string="Weighted Mark",
        compute="_compute_weighted",
    )

    @api.onchange("mark", "coefficient")
    def _compute_weighted(self):
        for record in self:
            record.weighted_mark = record.mark * int(record.coefficient)

    @api.constrains('mark')
    def _check_mark(self):
        for record in self:
            if record.mark < 0 or record.mark > 20:
                raise ValidationError(_("Invalid Grade"))


class StudentsStudentContinuous(models.Model):
    _name = "students.continuous"
    _inherit = "students.student"
    company = fields.Many2one(
        string="Company",
        comodel_name="res.partner",
        ondelete="set null",
    )
