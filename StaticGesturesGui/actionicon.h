#ifndef ACTIONICON_H
#define ACTIONICON_H

#include <QObject>
#include <QLabel>
#include <QString>

class ActionIcon : public QLabel
{
    Q_OBJECT
public:
    ActionIcon(QWidget *parent = 0);
    void setSize(int w = 50, int h = 50);
protected:
    void mousePressEvent(QMouseEvent *);

signals:
    void clicked(ActionIcon *p);
};

#endif // ACTIONICON_H
