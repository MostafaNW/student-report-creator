from inputparser import InputParser
class DataQuerier:
    """Performs queries on parsed csv data

    Parameters
    ----------
    data_dir : str
        The target directory where all the csv files are located.

    Attributes
    ----------
    students : dict
        Map of student information, indexed by the student_id.
    courses : dict
        Map of course information, indexed by the course_id.
    tests : dict
        Map of test information, indexed by the test_id.
    marks : dict
        Map of student test results for each course, indexed by the student_id.
    data_dir
    """
    def __init__(self, data_dir):
        input_parser = InputParser(data_dir)
        self.data_dir = data_dir
        self.students = input_parser.parse_students()
        self.courses = input_parser.parse_courses()
        self.tests = input_parser.parse_tests()
        self.marks = input_parser.parse_marks(self.tests, self.courses)
    def calculate_average(self, student_id):
        """Short summary.

        Parameters
        ----------
        student_id : str
            A student's unique ID

        Returns
        -------
        list
            an array of tuples of the form (course_id, final_mark)

        """
        #course_ids => array of (test_mark, weight)
        if student_id not in self.marks: return None
        marks = self.marks[student_id]
        #check for proper weight amount for all courses
        for _ ,test_tuples in marks.items():
            if not self.all_completed(test_tuples):
                raise Exception("ImproperWeightException: The weight total is not 100%")
        # function for applying a test mark's weight
        weigh_courses = lambda course_avg_list: \
                list(map( lambda mtuple: mtuple[0] * mtuple[1]/100 , course_avg_list) )
        #calculates the final mark in each course
        return list(map( lambda course_id: ( course_id, sum( weigh_courses(marks[course_id]) ) ), marks.keys() ) )
    def get_courses(self, student_id):
        """Short summary.

        Parameters
        ----------
        student_id : str
            A student's unique ID

        Returns
        -------
        str
            The report card, properly formated, for the student

        """
        student_name = self.students[student_id]['name']
        course_list = self.calculate_average(student_id)
        if course_list == None: return str() #empty string, student did not take any courses
        total_avg = self.calculate_total_avergage(course_list)
        formated_string = 'Student Id: {}, name: {}\nTotal Average:\t{}%\n\n'\
                            .format(student_id, student_name, self.calculate_total_avergage(course_list))
        #sort the courses based on id, the lambda just takes the first element of the tuple; course_id
        course_list.sort(key=lambda x: int(x[0]))
        for course_item in course_list:
            course_id = course_item[0]
            course_name = self.courses[course_id]['name']
            course_teacher = self.courses[course_id]['teacher']
            course_string = '\tCourse: {}, Teacher: {}\n\tFinal Grade:\t{}%\n\n'\
                    .format(course_name, course_teacher, "%.2f" % course_item[1])
            formated_string += course_string
        return formated_string

    def calculate_total_avergage(self, course_list):
        """Short summary.

        Parameters
        ----------
        course_list : list
            An array of tuples of the form (course_name, final_mark).

        Returns
        -------
        str
            The student's total average over all their courses, formated to two deicmal places

        """
        all_marks = list(map(lambda course_data: course_data[1], course_list))
        return "%.2f" % (sum(all_marks)/len(all_marks))

    def all_student_information(self):
        """Gets all student report card information.

        Parameters
        ----------


        Returns
        -------
        str
            string formated final report

        """
        results = str()
        all_students = list(self.students.keys())
        #ensure that the students are in proper order
        all_students.sort()
        for student_id in all_students: results += self.get_courses(student_id)
        return results
    def write_report(self):
        """Writes the report to the data_directory/output.txt

        Parameters
        ----------


        Returns
        -------
        None

        """
        report = self.all_student_information()
        try:
            with open(f"{self.data_dir}/output.txt", "w") as text_file:
                text_file.write(report)
        except Exception as e:
            print(e)
    def all_completed(self, weights):
        """checks to see if the weights add up to 100.

        Parameters
        ----------
        weights : list
            list of (mark, weight) tuples.

        Returns
        -------
        bool
            whether the weights total to 100% or not

        """
        weights = map(lambda tuple: tuple[1], weights)
        return sum(weights) == 100
