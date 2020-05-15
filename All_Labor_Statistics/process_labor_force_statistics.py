class Series:
    info = dict()
    values = dict()
    name = ""
    def __init__(self, series_line, category_names, categories):
        try:
            series_line = series_line.replace(" ", "")
            series_line += '\t'
            i = 0
            while True:
                data_type, series_line = series_line.split('\t', 1)
                data_type_name = category_names[i]
                if (data_type_name != "series_title"): # Unnecessary as series was combined into one dictionary
                    if (i == 0):
                        self.name = data_type # To assign the series its ID
                    if (data_type_name == "footnote" and data_type == ""): # As there is no code if there is no footnote in the Labor_Statistics_Classifications.txt file
                        self.info[data_type_name] = "No footnote"
                    elif (data_type_name[0:3] == "beg" or data_type_name[0:3] == "end"): # For begin_year, begin_period, ending_year, and ending_period which have no logged codes
                        self.info[data_type_name] = data_type.strip() # The strip is to remove the newline character at the end of ending_period
                    else:
                        self.info[data_type_name] = categories.get(data_type_name)[data_type]
                if (series_line == ""):
                    break
                i += 1
        except:
            print("Error")
    def add_values(self, time, value):
        self.values[time] = value
        
# Separates the categories into elements of a list
def generate_categories(categories_line):
    try:
        categories_line += ' ' # To acquire the last data category in the list as the split requires a trailing whitespace
        data_categories = []
        while True:
            lhs, categories_line = categories_line.split(' ', 1)
            if (categories_line == ""):
                break
            if (lhs[-5:] == "_code"):
                lhs = lhs[:-5]
            elif (lhs[-6:] == "_codes"):
                lhs = lhs[:-6]
            data_categories.append(lhs)
        return data_categories
    except FileNotFoundError:
        print("File not found in current directory!")
    except:
        print("Error generating data categories")

def store_categories(category_names):
    categories = dict()
    for i in category_names:
        try:
            if (i[0:6] == "series"):
                category_file = open("ln." + i[0:6] + ".txt")
            elif (i[0:3] != "beg" and i[0:3] != "end"):
                category_file = open("ln." + i + ".txt")
            if (i[0:6] != "series"):
                category_file.readline() # To strip the title line
                specific_category = dict()
                while True:
                    classification_line = category_file.readline()
                    if (classification_line == ""):
                        break
                    lhs, classification_line = classification_line.split('\t', 1) # To store the code's ID
                    lhs = lhs.strip()
                    classification_line = classification_line.strip() # To store the code's descriptor
                    specific_category[lhs] = classification_line
                    categories[i] = specific_category
            else: # For the series category data
                if i in categories: # Series has already been filled
                    break
                category_file.readline() # To strip the title line
                specific_category = dict()
                while True:
                    classification_line = category_file.readline()
                    if (classification_line == ""):
                        break
                    lhs, classification_line = classification_line.split('\t', 1) # To store the series ID
                    lhs = lhs.strip()
                    garbage, classification_line = classification_line.split('\t', 1) # To get to the series title
                    garbage, classification_line = classification_line.split('\t', 1)
                    classification_line, garbage = classification_line.split('\t', 1)
                    specific_category[lhs] = classification_line
                    categories[i] = specific_category
        except FileNotFoundError:
            print("File not found in current directory!")
        except:
            print("Problem generating category maps")
    return categories

def organize_categories(categories):
    classif_file = open("All_Category_Classifications.txt", 'w')
    for i in categories:
        print(i + ":", file = classif_file) # All Category Classifications
        for key, value in categories.get(i).items():
            print("\t" + key + ": " + value, file = classif_file)
    classif_file.close()

def main():        
    full_text = open("Labor_Statistics_Classifications.txt")
    category_names = generate_categories(' '.join(full_text.readline().split()) + ' ') # Retrieves first line of file, which contains the data categories
    categories = store_categories(category_names)
    organize_categories(categories)
    samples = []
    while True:
        series_line = full_text.readline()
        if (series_line == ""):
            break;
        sample = Series(series_line, category_names, categories)
        samples.append(sample)
    raw_data = open("raw_data.txt")
    raw_data.readline() # Discards the first line which names the column titles
    full_data = dict()
    i = 0
    index = 0
    while True:
        entry = raw_data.readline()
        if (entry == ""):
            break        
        entry = entry.replace(" ", "")
        entry += '\t' # Since our parser will require a trailing tab for every entry
        id_code, entry = entry.split('\t', 1)
        year, entry = entry.split('\t', 1)
        month_or_quarter, entry = entry.split('\t', 1)
        value, entry = entry.split('\t', 1)
        time = year + "_" + month_or_quarter
        if (samples[index].name != id_code):
            index += 1
        samples[index].add_values(time, value)
        # Used to generate the data with its name
        # print(samples[index].info["series_id"] + "," + time + "," + value)
        print(samples[index].name + "," + time + "," + value)

        
main()
