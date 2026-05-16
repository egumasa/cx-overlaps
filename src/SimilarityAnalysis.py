import sys, argparse
from IRSystem import IRSystem
from BaseFreqDictReader import TrigramFreqDictReader, UnigramFreqDictReader


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def Run():
    descr = """Compute Jaccard and Cosine similarities of tokens in a text like trigrams of words.
    E.g., SimilarityAnalysis -t trigram -d "C:\pos"
    """
    parser = DefaultHelpParser(description=descr)
    parser.add_argument(
        '--type',
        '-t',
        dest="analysisType",
        default=True,
        help='the type of analysis: unigram or trigram. Default is unigram.')
    parser.add_argument('--directory',
                        '-d',
                        dest="directoryOfTexts",
                        help='the directory path containing the input files.',
                        required=True)
    parser.add_argument('--use-semi-colon-delimiters',
                        dest='useSemiColonDelimiters',
                        action='store_true')
    parser.add_argument(
        '--output-directory',
        '-o',
        dest="outputDirectory",
        help='the directory path to store the overlapping tokens.')
    parser.add_argument(
        '-abc',
        dest='compare_abc',
        action='store_true',
        help=
        'If set then it will compare between a, b and c, otherwise deliveries.'
    )
    parser.add_argument(
        "--begin-line",
        dest="begin_line",
        type=int,
        help=
        "Start reading the input files from this line. Useful to have metadata in the files that we want to ignore."
    )
    parser.add_argument(
        "--compare-to-source",
        "-model",
        dest="compSource",
        type=bool,
        help="compare to source rather than between performances.",
        default=False)
    parser.add_argument("--source-text-path",
                        "-s",
                        dest="sourcePath",
                        type=str,
                        help="Path to the source text.")
    parser.add_argument("--output-name",
                        "-oname",
                        dest="outName",
                        type=str,
                        help="This is outputname")

    args = parser.parse_args()
    extension = ".cex"  # default
    analysisType = args.analysisType
    directoryOfTexts = args.directoryOfTexts  # C:\temp\*.txt
    useSemiColonDelimiters = args.useSemiColonDelimiters
    outputDirectory = args.outputDirectory
    compare_abc = args.compare_abc
    begin_line = args.begin_line
    compare_to_source = args.compSource  # Added on May 27, 2022
    sourceFilePath = args.sourcePath  # Added on May 27, 2022
    outputName = args.outName  # Added on May 27, 2022

    pathAsArray = directoryOfTexts.split("*")
    if len(pathAsArray) == 2 and pathAsArray[1].startswith(".") and (
            pathAsArray[0].endswith("\\") or pathAsArray[0].endswith("/")
    ):  # is the path of the form C:\temp\*.txt
        extension = pathAsArray[1]  # .txt
        directoryOfTexts = pathAsArray[0]  # C:\temp\

    if analysisType == "trigram":
        fdr = TrigramFreqDictReader(directoryOfTexts, extension, compare_abc,
                                    begin_line)  #this reads the Trigram
    else:
        fdr = UnigramFreqDictReader(directoryOfTexts, extension, compare_abc,
                                    begin_line)

    # when compare_abc, the student key is {cond}_{studentId}_{delivery}
    # when compare_abc is false, the student key is {cond}_{studentId}_{session}
    filesGroupedByStudents = fdr.GetFilesGroupedByStudents()

    ir = IRSystem(fdr)
    similaritiesPerStudent = {}
    for studentKey in filesGroupedByStudents:
        if studentKey not in similaritiesPerStudent:  #initialize dict for each studentkey
            similaritiesPerStudent[studentKey] = {}
        #calculate similarity here

        if compare_to_source:
            j = fdr.CompareToSource(filesGroupedByStudents[studentKey],
                                    sourceFilePath, ir.JaccardSimilarity,
                                    "JaccardSimilarity")
            for comparison in j:
                similaritiesPerStudent[studentKey][comparison] = j[comparison]
            c = fdr.CompareToSource(filesGroupedByStudents[studentKey],
                                    sourceFilePath, ir.CosineSimilarity,
                                    "CosineSimilarity")
            for comparison in c:
                similaritiesPerStudent[studentKey][comparison] = c[comparison]

        else:
            j = fdr.CompareFiles(filesGroupedByStudents[studentKey],
                                 ir.JaccardSimilarity, "JaccardSimilarity")
            for comparison in j:
                similaritiesPerStudent[studentKey][comparison] = j[comparison]
            c = fdr.CompareFiles(filesGroupedByStudents[studentKey],
                                 ir.CosineSimilarity, "CosineSimilarity")
            for comparison in c:
                similaritiesPerStudent[studentKey][comparison] = c[comparison]

        if (outputDirectory is not None):
            fdr.GenerateTokenIntersections(filesGroupedByStudents[studentKey],
                                           outputDirectory)

    # Added on May 27, 2022: New output function
    with open(outputName, 'w') as outf:
        outf.write("Condition,StudentId,SessionPair,Measure,Score\n")
        for studentKey, similarities in similaritiesPerStudent.items():
            key_parts = studentKey.split("_")
            condition = key_parts[0]
            studentId = key_parts[1]
            for measure_key, value in similarities.items():
                # measure_key format: "MeasureName_session1_session2"
                parts = measure_key.split("_")
                measure = parts[0]
                session_pair = "_".join(parts[1:])
                outf.write(",".join([
                    str(condition),
                    str(studentId),
                    str(session_pair),
                    str(measure),
                    str(value)
                ]))
                outf.write("\n")

    #print(similaritiesPerStudent)
    ## File output

    # delimeter = ","
    # if (useSemiColonDelimiters):
    #     delimeter = ";"
    # comparisons = set([])  #this is

    # for studentKey in similaritiesPerStudent:  #this is dictionary with studentkey
    #     similarities = ""
    #     for comparison in sorted(similaritiesPerStudent[studentKey].keys()):
    #         similarities += comparison + "_" + str(
    #             similaritiesPerStudent[studentKey][comparison]) + delimeter
    #         if comparison not in comparisons:
    #             comparisons.add(comparison)
    #     row = str.format("{0}{2}{1}{2}",
    #                      delimeter.join(str.split(studentKey, "_")),
    #                      similarities, delimeter)
    #     # print(row)

    # comparisons = sorted(comparisons)
    # headerRow = []
    # headerRow.append("Condition")
    # headerRow.append("StudentId")
    # headerRow.append("Session")
    # for comparison in comparisons:
    #     headerRow.append(comparison)

    # print(delimeter.join(headerRow))
    # rows = {}
    # for studentKey in similaritiesPerStudent:
    #     row = delimeter.join(str.split(studentKey, "_")) + delimeter
    #     for comparison in comparisons:
    #         similarities = similaritiesPerStudent[studentKey]
    #         if comparison in similarities:
    #             row += str(similarities[comparison]) + delimeter
    #         else:
    #             row += delimeter
    #     print(row)
    #     rows[studentKey] = row


Run()
