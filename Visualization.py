import matplotlib.pyplot as plt
import seaborn as sns

class Visualization:
    def __init__(self) -> None:
        pass
    def pieChart(self, coreData):
        colors = sns.color_palette('bright')
        plt.pie(coreData['total coin value'], labels=coreData['symbol'],colors = colors, autopct = '%0.0f%%', labeldistance=1.3)
        plt.show()
        def BTCvsIndex(df):
            ...
