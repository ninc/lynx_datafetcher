

class QualityInstruments:

    def __init__(self):
        pass

    def read_file(self, filepath):
        with open(filepath) as file:
            for line in file:
                print(line)



if __name__ == '__main__':
    q = QualityInstruments()
    q.read_file('../kvalitetsbolag.txt')