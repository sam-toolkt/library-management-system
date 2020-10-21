from odoo import models, fields, api, exceptions



class Library(models.Model):
	_name = 'library.books'

	_description = 'Brussels Library'

	name = fields.Char(string="ISBN", required=False)
	# author = fields.Char(string="Author", required=False)
	# editor = fields.Char(string="Editor", required=False)
	year = fields.Char(string="Year of Edition", required=False)
	book_name = fields.Char(string="Book Title", required=False)
	# summary= fields.Text()
	# stock_of_books = fields.Integer(string="Number of Books")


	instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])

	librarian_id = fields.Many2one('res.users', string="Library Admin", index=True)
	about_ids = fields.Many2many('library.about', ondelete="cascade", string="About", required=True)

	taken_books = fields.Float(string="Taken Books", compute='_taken_books')

	def copy(self, default=None):
		default = dict(default or {})

		copied_count = self.search_count(
			[('name', '=like', u"Copy of {}%".format(self.name))])
		if not copied_count:
			new_name = u"Copy of {}".format(self.name)
		else:
			new_name = u"Copy of {} ({})".format(self.name, copied_count)

		default['name'] = new_name
		return super(Library, self).copy(default)

	_sql_constraints = [
		('name_description_check',
			'CHECK(name != description)',
			"The title of the books should not be the description"),

			('name_unique',
			'UNIQUE(name)',
			"The course title must be unique"),
	]

class Rental(models.Model):
	_name = 'library.rentals'
	# _inherit = 'library.books'
	_description = "Book Rentals"
	# _inherits = {'library.books': 'librarian_id'}


	# name = fields.Many2one('library.members', ondelete="cascade", string="Borrower's Name", required=False)
	name = fields.Many2one('res.partner', ondelete="cascade", string="Borrower's Name")
	lib_info = fields.Char(string="Library ID", required=False)
	start_date = fields.Date()
	end_date = fields.Float(digits=(6, 0), help="Duration in days")
	available = fields.Integer(string="Stock")
	active = fields.Boolean(default=True)

	librarian_id = fields.Many2one('res.users', string="Library on Duty", index=True)
	book_ids = fields.Many2many('library.books', ondelete="cascade", string="Records", required=True)
	

	taken_books = fields.Float(string="Taken Books", compute='_taken_books')

	@api.depends('available', 'book_ids')
	def _taken_books(self):
		for r in self:
			if not r.available:
				r.taken_books = 0.0
			else:
				r.taken_books = 100.0 * len(r.book_ids) / r.available


	@api.onchange('available', 'books_ids')
	def _verfy_books(self):
		if self.available < 0:
			return{
			'warning':{
					'title': "Incorrect valaue",
					'message': "The number of available books may not be negative"
				}
			}
		if self.available < len(self.book_ids):
			return{
				'warning':{
					'title': "Book Error",
					'message': "Increase or remove excess books"
				}
			}

	
class About(models.Model):
	_name =  'library.about'
	_description = "Authors Editors"


	author=fields.Char(string="Author/s", required=False)
	# author=fields.Char(string="Author/s", required=False)
	editor=fields.Char(string="Editor/s", required=False)
	summary = fields.Text()

	# isbn_id = fields.Many2one('library.books.isbn', ondelete="cascade", string="ISBN", required=False)
	# member_id = fields.Many2one('library.members', ondelete="cascade", string="Borrower's Name", required=False)
 	# taken_books = fields.Float(string="Taken Books", compute="_taken_books")

    # @api.depends('available', 'stock_of_books')
    # def _taken_books(self):
    #     for r in self:
    #         if not r.available:
    #             r.taken_books = 0.0
    #         else:
    #             r.taken_books = stock_of_books - available
    
    # @api.depends('available', 'book_ids')
    # def _taken_books(self):
    # 	for r in self:
    # 		if not r in self:
    # 			r.taken_books = 0.0
    # 		else:
    # 			r.taken_books = 100 * len(r.book_ids)/r.api
    

# class Librarian(models.Model):
# 	_name = "library.librarian"
# 	_description = "Library Librarian"

# 	name = fields.Char(string="First Name", required=True)
# 	lname = fields.Char(string="Last Name", required=False)
# 	phone = fields.Char(string="Phone", required=False)
# 	email = fields.Char(string="Email", required=False)
# 	lib_info = fields.Char(string="Librarian ID", required=False)
# 	address = fields.Text(string="Address", required=False)

# class Member(models.Model):
# 	_name = "library.members"
# 	_description = "Library Member"

# 	name = fields.Char(string="First Name", required=False)
# 	lname = fields.Char(string="Last Name", required=False)
# 	phone = fields.Char(string="Phone", required=False)
# 	email = fields.Char(string="Email", required=False)
# 	visit_info = fields.Char(string="Library ID", required=False)
# 	address = fields.Text(string="Address", required=False)
# 	