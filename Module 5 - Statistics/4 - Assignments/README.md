**5.4.1 - One Sided Test**

Complete the one-sided-tests function. It is provided a list of file that contain samples from a distribution. 
The function should return those file names where the sample rejects the NULL hypothesis during a one-sided t-test.

    def one_sided_tests(_files: list, _mean: float, _alpha: float, _less_than: bool):
        Conduct a one-sided t-test, either left or ride sided. Null hypothesis is the means are equal.
        :param _files: List of files to be tested. Assume they can be loaded directly as a numpy array
        :param _mean: The test statistic mean for the hypothesis
        :param _alpha: Desired alpha value for t-test
        :param _less_than: If true, then a left-sided (<) t-test is performed. Otherwise, a right-sided test (>)
        :return: A list of files where the null hypothesis is rejected
