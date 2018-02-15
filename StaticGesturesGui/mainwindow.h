#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QProcess>
#include "gestureicon.h"
#include "actionicon.h"
#include <QMap>
#include <QPushButton>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

    void addActionIcon(QString text);
    void addGestureIcon(QString path);

protected:
    void paintEvent(QPaintEvent *);

private:
    Ui::MainWindow *ui;
    QVector <GestureIcon *> GesturIcons;
    QVector <ActionIcon *> ActionIcons;
    int selectedGesture;
    int iconSize;
    QVector <int> gestureMatching;
    QVector <int> actionMatching;
    QMap <GestureIcon *, int> gestureMapping;
    QMap <ActionIcon *, int> actionMapping;

    void addGestures();
    void addActions();

    void updatePositions();
    void markSelected(GestureIcon *p);
    void markUnSelected(GestureIcon * p);
    QPoint getGesturePoint(GestureIcon * p);
    QPoint getActionPoint(ActionIcon * p);

    QPushButton *startButton;

public slots:
    void onGestureIconClicked(GestureIcon * p);
    void onActionIconClicked(ActionIcon * p);
    void onStartButtonClicked(bool);
};

#endif // MAINWINDOW_H
