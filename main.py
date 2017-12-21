from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (6,6)
import numpy as np
import time
import sys
import os
import threading
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL, pyqtSignal
from DNA import main as DNA
from population import main as Population
os.system('pyuic4 -x GUI.ui -o GUI.py')
from GUI import Ui_M_W as UI


class GA_thread(QThread):
    log_sig = pyqtSignal(list)
    answer_sig = pyqtSignal()
    def __init__(self, dna_n, pop_len, mut_rate, max_iter):
        QThread.__init__(self)
        self.dna_n = dna_n
        self.pop_len = pop_len
        self.mut_rate = mut_rate
        self.max_iter = max_iter
        self.stop_flag = False


    def __del__(self):
        self.quit()
        self.wait()


    def stop(self):
        self.stop_flag = True


    def run(self):
        t0 = time.time()
        population = Population(dna_n=self.dna_n, pop_len=self.pop_len, mutation_rate=self.mut_rate, max_iter=self.max_iter)
        population.initialize()
        population.fitness_measure()

        while True:
            if self.stop_flag:
                break
            try:
                population.selection()
                population.fitness_measure()
                population.evaluate()
                avg_score = np.average(population.score)
                # print('generation : {0:5d}  ,  average fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, avg_score, (avg_score/population.max_score)*100, population.get_answer()[0]))
                log = [population.generation_num, avg_score, (avg_score/population.max_score)*100, population.get_answer()[0]]
                self.log_sig.emit(log)
            except ValueError as e:
                if str(e) == 'Bad Population':
                    # print('\n\n', e)
                    self.log_sig.emit(['\nBad Population!'])
                    break
                else:
                    self.Answer = population.get_answer()
                    # print('\n\ngeneration : {0:5d}  ,  Answer fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, Answer[1], (Answer[1]/population.max_score)*100, Answer[0]))
                    log = [population.generation_num, self.Answer[1], (self.Answer[1]/population.max_score)*100, self.Answer[0]]
                    self.log_sig.emit(log)

                    self.log_sig.emit(['\nTime : {}s'.format(round(time.time() - t0, 2))])

                    self.answer_sig.emit()

                    break


class main(QtGui.QMainWindow, UI):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.run_btn.clicked.connect(self.input_check_starter)


    def input_check_starter(self):
        try:
            self.GA.stop()
        except:
            pass
        self.log_output.clear()
        self.log_queens.clear()

        try:
            self.d_dna_n = int(self.qnum.text())
            self.d_pop_len = int(self.pop_len.text())
            self.d_mut_rate = int(self.mut_rate.text()) / 100
            self.d_max_iter = int(self.max_iter.text())
        except Exception as e:
            self.logger(['Entered Numbers Error!'])
            return

        self.GA = GA_thread(dna_n=self.d_dna_n, pop_len=self.d_pop_len, mut_rate=self.d_mut_rate, max_iter=self.d_max_iter)
        self.GA.log_sig.connect(self.logger)
        self.GA.answer_sig.connect(self.done)

        self.stop_btn.clicked.connect(self.GA.stop)
        self.GA.start()



    def logger(self, log):
        log = list(log)
        log_len = len(log)

        if log_len == 4:
            log_style = 'generation : {0:6d}   ,   average fitness : {1:10.2f}     {2:3.2f}%'
            self.log_output.appendPlainText(log_style.format(log[0], log[1], log[2]))
            self.log_queens.appendPlainText('g{0:6d} => '.format(log[0]) + ', '.join([str(x+1) for x in log[3]]))
        elif log_len == 1:
            self.log_output.appendPlainText(log[0])


    def plot_stuf(self):

        plot_ans = np.zeros([self.d_dna_n, self.d_dna_n])

        for r, x in enumerate(plot_ans):
            for c, y in enumerate(x):
                if (r + c) % 2 == 0:
                    plot_ans[r, c] = 1

        plt.cla()
        plt.imshow(plot_ans,cmap='gray', interpolation='nearest',
                    extent=(0.5, self.d_dna_n + 0.5, 0.5, self.d_dna_n + 0.5))
        row_labels = col_labels = range(1, self.d_dna_n + 1)
        plt.xticks(range(1, self.d_dna_n + 1), col_labels)
        plt.yticks(range(1, self.d_dna_n + 1), row_labels)
        plt.xlim(0.5, self.d_dna_n + 0.5)
        plt.ylim(0.5, self.d_dna_n + 0.5)
        ax = plt.gca()
        for line in ax.xaxis.get_ticklines():
            line.set_visible(False)
        for line in ax.yaxis.get_ticklines():
            line.set_visible(False)

        plot_matrix = self.GA.Answer[0] + 1

        plt.title('{} Queens'.format(self.d_dna_n))
        plt.grid(False)
        plt.scatter(range(1,self.d_dna_n+1), plot_matrix, color='red', s=4000//self.d_dna_n)

        # plt.show()
        plt.savefig('N_Q_Answer.png')

        pixmap = QtGui.QPixmap('N_Q_Answer.png')
        self.log_shape.setPixmap(pixmap)
        # os.remove('N_Q_Answer.png')


    def done(self):
        QtGui.QMessageBox.information(self, "Done!", "Answer Found!")
        self.plot_stuf()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
    form = main()
    form.showMaximized()
    app.exec_()
