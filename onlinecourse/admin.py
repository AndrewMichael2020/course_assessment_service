from django.contrib import admin                # Import Django's admin module to customize the admin interface
# <HINT> Import any new Models here             # Developer note: import additional models if needed
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission  # Import specified models from the local models module

# <HINT> Register QuestionInline and ChoiceInline classes here  # Developer note: register inline admin classes for Question and Choice

class LessonInline(admin.StackedInline):        # Define an inline admin class for the Lesson model using a stacked layout
    model = Lesson                              # Set Lesson as the model for inline editing
    extra = 5                                   # Display 5 extra blank Lesson forms in the admin interface

# Register your models here.                    # Comment indicating the start of model registration with the admin site
class CourseAdmin(admin.ModelAdmin):            # Define a custom admin class for the Course model
    inlines = [LessonInline]                    # Include inline Lesson forms on the Course admin page
    list_display = ('name', 'pub_date')         # Display 'name' and 'pub_date' columns in the Course list view
    list_filter = ['pub_date']                  # Add a filter sidebar for 'pub_date' in the Course admin
    search_fields = ['name', 'description']     # Enable search on 'name' and 'description' fields in the Course admin

class LessonAdmin(admin.ModelAdmin):            # Define a custom admin class for the Lesson model
    list_display = ['title']                    # Display the 'title' column in the Lesson list view

# <HINT> Register Question and Choice models here  # Developer note: register admin classes for Question and Choice

class ChoiceInline(admin.StackedInline):         # Define an inline admin class for the Choice model using a stacked layout
    model = Choice                              # Set Choice as the model for inline editing
    extra = 2                                   # Display 2 extra blank Choice forms in the admin interface

class QuestionInline(admin.StackedInline):       # Define an inline admin class for the Question model using a stacked layout
    model = Question                            # Set Question as the model for inline editing
    extra = 2                                   # Display 2 extra blank Question forms in the admin interface

class QuestionAdmin(admin.ModelAdmin):           # Define a custom admin class for the Question model
    inlines = [ChoiceInline]                    # Include inline Choice forms on the Question admin page
    list_display = ['content']                  # Display the 'content' column in the Question list view

admin.site.register(Course, CourseAdmin)         # Register the Course model with the admin site using CourseAdmin
admin.site.register(Lesson, LessonAdmin)         # Register the Lesson model with the admin site using LessonAdmin
admin.site.register(Instructor)                  # Register the Instructor model with default admin options
admin.site.register(Learner)                     # Register the Learner model with default admin options
admin.site.register(Question, QuestionAdmin)     # Register the Question model with the admin site using QuestionAdmin
admin.site.register(Choice)                      # Register the Choice model with default admin options
admin.site.register(Submission)                  # Register the Submission model with default admin options
