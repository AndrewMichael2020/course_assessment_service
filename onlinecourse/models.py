import sys                                      # Provides system-specific functions and parameters
from django.utils.timezone import now           # Imports the current time function from Django's timezone utilities
try:
    from django.db import models                # Attempts to import Django's ORM models module for defining database models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")  # Prints error if Django isn't installed or fails to load
    sys.exit()                                  # Exits the program if the import fails

from django.conf import settings                  # Imports Django's settings to access configuration (e.g., AUTH_USER_MODEL)
import uuid                                       # Imports the UUID module for generating unique identifiers (not used in this snippet)

# Instructor model
class Instructor(models.Model):                   # Defines the Instructor model inheriting from Django's base model
    user = models.ForeignKey(                    # Creates a foreign key linking each instructor to a user account
        settings.AUTH_USER_MODEL,                # References the user model defined in Django settings
        on_delete=models.CASCADE,                # Deletes the instructor record if the associated user is deleted
    )
    full_time = models.BooleanField(default=True) # Boolean field indicating if the instructor is full-time (defaults to True)
    total_learners = models.IntegerField()         # Integer field to store the total number of learners taught

    def __str__(self):                             # Method to define the string representation of an Instructor instance
        return self.user.username                  # Returns the username of the associated user

# Learner model
class Learner(models.Model):                      # Defines the Learner model
    user = models.ForeignKey(                    # Creates a foreign key linking each learner to a user account
        settings.AUTH_USER_MODEL,                # References the user model from Django settings
        on_delete=models.CASCADE,                # Deletes the learner record if the associated user is deleted
    )
    STUDENT = 'student'                           # Constant representing a student occupation
    DEVELOPER = 'developer'                       # Constant representing a developer occupation
    DATA_SCIENTIST = 'data_scientist'               # Constant representing a data scientist occupation
    DATABASE_ADMIN = 'dba'                        # Constant representing a database admin occupation
    OCCUPATION_CHOICES = [                        # List of tuples defining available occupation choices
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(               # Character field to store the occupation with restricted choices
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,               # Restricts the field to predefined occupation choices
        default=STUDENT                           # Sets default occupation to 'student'
    )
    social_link = models.URLField(max_length=200)  # URL field to store a link to the learner's social profile

    def __str__(self):                             # Defines the string representation of a Learner instance
        return self.user.username + "," + self.occupation  # Returns a string combining username and occupation

# Course model
class Course(models.Model):                       # Defines the Course model
    name = models.CharField(null=False, max_length=30, default='online course')  # Char field for course name with a default value
    image = models.ImageField(upload_to='course_images/')  # Image field for the course, saving files to the 'course_images/' directory
    description = models.CharField(max_length=1000)  # Char field for course description
    pub_date = models.DateField(null=True)         # Date field for the publication date; can be null
    instructors = models.ManyToManyField(Instructor)  # Many-to-many relationship with the Instructor model
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')  # Many-to-many relationship with User model via the Enrollment model
    total_enrollment = models.IntegerField(default=0)  # Integer field to count total enrollments, defaulting to 0
    is_enrolled = False                           # Non-model attribute (plain Python attribute) indicating enrollment status

    def __str__(self):                             # Defines the string representation of a Course instance
        return "Name: " + self.name + "," + "Description: " + self.description  # Returns a string with course name and description

# Lesson model
class Lesson(models.Model):                       # Defines the Lesson model
    title = models.CharField(max_length=200, default="title")  # Char field for the lesson title with a default value
    order = models.IntegerField(default=0)         # Integer field to specify the order of lessons, defaulting to 0
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key linking a lesson to a course; cascade deletion applies
    content = models.TextField()                   # Text field for the lesson content

# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):                   # Defines the Enrollment model to track course enrollments
    AUDIT = 'audit'                             # Constant representing audit mode enrollment
    HONOR = 'honor'                             # Constant representing honor mode enrollment
    BETA = 'BETA'                               # Constant representing beta mode enrollment
    COURSE_MODES = [                            # List of tuples defining enrollment mode choices
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Foreign key linking to a User; cascade deletion applies
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key linking to a Course; cascade deletion applies
    date_enrolled = models.DateField(default=now)  # Date field recording when the enrollment occurred; defaults to current time
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)  # Char field for enrollment mode, limited to predefined choices with a default of audit
    rating = models.FloatField(default=5.0)         # Float field for course rating, defaulting to 5.0

class Question(models.Model):                     # Defines the Question model for assessments
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key linking a question to a course; cascade deletion applies
    content = models.CharField(max_length=200)      # Char field for the question content
    grade = models.IntegerField(default=50)         # Integer field for the grade/weight of the question, defaulting to 50

    # method to calculate if the learner gets the score of the question
    def __str__(self):                            # String representation method for Question
        return "Question: " + self.content         # Returns the question content prefixed with "Question: "

    def is_get_score(self, selected_ids):         # Method to determine if the learner's selected choices yield full marks
        all_answers = self.choice_set.filter(is_correct=True).count()  # Counts all correct choices for this question
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()  # Counts correct choices selected by the learner
        if all_answers == selected_correct:         # If learner selected all correct choices...
            return True                             # ...return True indicating full score
        else:
            return False                            # Otherwise, return False

class Choice(models.Model):                       # Defines the Choice model for each question option
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Foreign key linking a choice to a question; cascade deletion applies
    content = models.CharField(max_length=200)      # Char field for the content of the choice
    is_correct = models.BooleanField(default=False) # Boolean field indicating if the choice is correct; defaults to False

class Submission(models.Model):                   # Defines the Submission model to record exam submissions
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)  # Foreign key linking submission to an enrollment record; cascade deletion applies
    choices = models.ManyToManyField(Choice)       # Many-to-many field linking submission to selected choices

# Comments below explain potential alternative design or additional notes:
# One enrollment could have multiple submissions
# One submission could have multiple choices
# One choice could belong to multiple submissions
# The commented out Submission model below is an alternate (redundant) definition:
#class Submission(models.Model):
#    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
#    choices = models.ManyToManyField(Choice)
