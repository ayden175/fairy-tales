import csv
import os
import annotator.config as cfg

class DataSaver():
    def export_csv(self):
        directory = f'{cfg.path}/annotations'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = cfg.story.replace('.txt', '.csv')

        with open(f'{directory}/{filename}', 'w', newline='', encoding='utf-8') as f:
            # create the csv writer
            writer = csv.writer(f)

            header = ['word', 'entity', 'name', 'alignment']
            # write a row to the csv file
            writer.writerow(header)

            entity = 'O'
            prevName = ''

            for par in cfg.words:
                for word in par:
                    text = word.getText()
                    if text == '':
                        continue

                    if word.entity and (entity == 'O' or word.getName() != prevName):
                        entity = 'B'
                    elif word.entity and (entity == 'B' or entity == 'I'):
                        entity = 'I'
                    else:
                        entity = 'O'
                        prevName = ''
                        writer.writerow([text, entity, 'X', 'X'])
                        continue

                    prevName = word.getName()
                    writer.writerow([text, entity, word.getName(), word.getAlignment()])

        cfg.unsaved_changes = False