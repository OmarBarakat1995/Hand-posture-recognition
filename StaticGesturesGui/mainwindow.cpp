#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QDebug>
#include <QPainter>
#include <QProcess>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    iconSize = 60;
    selectedGesture = -1;

    setWindowTitle("Static Gesture Recognition");
    addGestures();
    addActions();

    updatePositions();

    startButton = new QPushButton(this);
    startButton->setText("Start");

    int buttonWidth = 100;
    int buttonHeight = 40;
    int x = (width() / 2) - (buttonWidth/2);
    int y = 50;

    startButton->setGeometry(QRect(x, y, buttonWidth, buttonHeight));

    connect(startButton, SIGNAL(clicked(bool)), this, SLOT(onStartButtonClicked(bool)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::addGestures()
{
    addGestureIcon("Images/one.jpg");
    addGestureIcon("Images/two.jpg");
    addGestureIcon("Images/swing.jpg");
    addGestureIcon("Images/fist.jpg");
    addGestureIcon("Images/five.jpg");
}

void MainWindow::addActions()
{
    addActionIcon("Up");
    addActionIcon("Down");
    addActionIcon("Left");
    addActionIcon("Right");
    addActionIcon("Stop");
}

void MainWindow::addGestureIcon(QString path)
{
    GestureIcon *g = new GestureIcon(this);
    g->setIcon(path);

    int cur = GesturIcons.size();
    GesturIcons.push_back(g);
    gestureMapping[g] = cur;

    //Equivalent Action to this gesture
    gestureMatching.push_back(cur);

    connect(g, SIGNAL(clicked(GestureIcon*)), this, SLOT(onGestureIconClicked(GestureIcon*)));
}

void MainWindow::addActionIcon(QString text)
{
    ActionIcon *a = new ActionIcon(this);
    a->setText(text);
    a->setStyleSheet("QLabel {border: 1px solid black}");

    int cur = ActionIcons.size();
    ActionIcons.push_back(a);
    actionMapping[a] = cur;

    // Equivalent Gesture to this action
    actionMatching.push_back(cur);

    connect(a, SIGNAL(clicked(ActionIcon*)), this, SLOT(onActionIconClicked(ActionIcon*)));
}

void MainWindow::onGestureIconClicked(GestureIcon *p)
{
    // current gesture index
    int cur_gesture = gestureMapping[p];

    if(cur_gesture == selectedGesture){
        markUnSelected(p);
        selectedGesture = -1;
        return;
    }
    // No Gesture Selected
    if(selectedGesture == -1){
        selectedGesture = cur_gesture;
        markSelected(p);
        return;
    }
    if(selectedGesture != cur_gesture){
        markUnSelected(GesturIcons[selectedGesture]);
        selectedGesture = cur_gesture;
        markSelected(p);
    }

}

void MainWindow::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    QPen pen = QPen(Qt::blue);
    pen.setWidth(5);

    painter.setPen(pen);

    for(int i = 0; i < GesturIcons.size(); i++){
        QPoint p1 = getGesturePoint(GesturIcons[i]);
        int ac = gestureMatching[i];
        if(ac == -1)
            continue;
        QPoint p2 = getActionPoint(ActionIcons[ac]);

        painter.drawLine(p1, p2);
    }

    //painter.drawLine(x, y, 5, 5);*/
}
void MainWindow::onActionIconClicked(ActionIcon *p)
{
    int cur_action = actionMapping[p];

    // No selected gesture
    if(selectedGesture == -1)
        return;
    // No Change
    if(actionMatching[cur_action] == selectedGesture)
        return;

    //GestureIcon *g = gestureMapping[selectedGesture];
    //qDebug() << "Selected Gesture: " << selectedGesture << "\n";

    //reset gesture
    if(gestureMatching[selectedGesture] != -1){
        int ac = gestureMatching[selectedGesture];
        actionMatching[ac] = -1;
        gestureMatching[selectedGesture] = -1;
    }
    //reset action
    if(actionMatching[cur_action] != -1){
        int g = actionMatching[cur_action];
        gestureMatching[g] = -1;
        actionMatching[cur_action] = -1;
    }

    actionMatching[cur_action] = selectedGesture;
    gestureMatching[selectedGesture] = cur_action;

    markUnSelected(GesturIcons[selectedGesture]);
    selectedGesture = -1;

    update();
}

void MainWindow::updatePositions()
{
    int dist_w = 0.4 * width() / 2;
    int dist_y = 100;

    // set position of gesture icons
    for(int i = 0; i < GesturIcons.size(); i++){
        GesturIcons[i]->setGeometry(QRect(dist_w, dist_y, iconSize, iconSize));
        GesturIcons[i]->setSize(iconSize, iconSize);
        dist_y += iconSize + 5;
    }

    dist_w = width() - dist_w - iconSize;
    dist_y = 100;

    for(int i = 0; i < ActionIcons.size(); i++){
        ActionIcons[i]->setGeometry(QRect(dist_w, dist_y, iconSize, iconSize));
        dist_y += iconSize + 5;
    }
}

void MainWindow::markSelected(GestureIcon *p)
{
    p->setStyleSheet("QLabel {border: 2px solid red}");
}

void MainWindow::markUnSelected(GestureIcon *p)
{
    p->setStyleSheet("QLabel {border: 0px solid red}");
}


QPoint MainWindow::getGesturePoint(GestureIcon *p)
{
    QPoint point = p->pos();
    //qDebug() << point.x() << " " << point.y() << "\n";
    int x = point.x() + iconSize;
    int y = point.y() + iconSize/2;
    point = QPoint(x, y);

    //qDebug() << point.x() << " " << point.y() << "\n";

    return point;
}

QPoint MainWindow::getActionPoint(ActionIcon *p)
{
    QPoint point = p->pos();
    int x = point.x();
    int y = point.y() + iconSize/2;
    point = QPoint(x, y);

    return point;
}

void MainWindow::onStartButtonClicked(bool)
{
    //qDebug() << "Start Button Clicked\n";
    QProcess p;
    QStringList params;
    //params << "pipeline.py" << "5" << "1" << "3" << "2" << "5" << "4";

    int num_gestures = 5;

    QString s = QString::number(num_gestures);

    params << "pipeline.py" << s;
    for(int i = 0; i < ActionIcons.size(); i++){
        int m = actionMatching[i] + 1;
        s = QString::number(m);
        params.append(s);
    }

    p.start("/home/ahmad/anaconda3/bin/python", params);
    p.waitForFinished(-1);
}
