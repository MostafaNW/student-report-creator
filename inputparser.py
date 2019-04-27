import csv

class InputParser:
    """Parser csv data into an easily accesible format using dictionaries (maps).

    Parameters
    ----------
    data_dir : str
        The target directory where all the csv files are located.

    Attributes
    ----------
    data_dir

    """
    def __init__(self, data_dir):
        self.data_dir = data_dir + '/'
    def parse_tests(self):
        """Loads the tests.csv into memory in a proper dictionary format.

        Parameters
        ----------


        Returns
        -------
        type
            Map of test_id => test_meta_data.

        """
        with open(self.data_dir + 'tests.csv', newline='') as csvfile:
            test_reader = csv.DictReader(csvfile)
            test_dict = dict()
            for test in test_reader:
                test_dict[test['id']] = {'course_id': test['course_id'], 'weight': float(test['weight'])}
            return test_dict
    def parse_courses(self):
        """Loads the courses.csv into memory in a proper dictionary format.

        Parameters
        ----------


        Returns
        -------
        dict
            Map of course_id => course_meta_data

        """
        with open(self.data_dir + 'courses.csv', newline='') as csvfile:
            course_reader = csv.DictReader(csvfile)
            course_dict = dict()
            for course in course_reader:
                course_dict[course['id']] = {'name': course['name'], 'teacher': course['teacher']}
            return course_dict
    def parse_marks(self, tests, courses):
        """Loads the marks.csv into memory in a proper dictionary format.

        Parameters
        ----------
        tests : dict
            Map of test_id => test_meta_data.
        courses : dict
            Map of course_id => course_meta_data

        Returns
        -------
        type
            Map of student_id => course_id => course_test_mark_meta_data
            course_test_mark_meta_data is a tuple of the form (course_mark, weight)
        """
        with open(self.data_dir + 'marks.csv', newline='') as csvfile:
            mark_reader = csv.DictReader(csvfile)
            mark_dict = dict() #key: student id
            for mark in mark_reader:
                student = mark['student_id']
                if student not in mark_dict:
                    mark_dict[student] = dict()
                test_id = mark['test_id']
                course_id = tests[test_id]['course_id']
                if course_id not in mark_dict[student]:
                    mark_dict[student][course_id] = list()
                mark_dict[student][course_id].append( (float(mark['mark']), \
                                                    tests[test_id]['weight']) )
            return mark_dict
    def parse_students(self):
        """Loads the students.csv into memory in a proper dictionary format..

        Parameters
        ----------


        Returns
        -------
        dict
            Map of student_id => student_meta_data

        """
        with open(self.data_dir + 'students.csv', newline='') as csvfile:
            student_reader = csv.DictReader(csvfile)
            student_dict = dict()
            for student in student_reader:
                student_dict[student['id']] = {'name': student['name'], 'course_ids': list()}
            return student_dict
