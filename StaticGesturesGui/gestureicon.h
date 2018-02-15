#ifndef GESTUREICON_H
#define GESTUREICON_H

#include <QObject>
#include <QLabel>
#include <QString>

class GestureIcon : public QLabel
{
    Q_OBJECT
public:
    GestureIcon(QWidget *parent = 0);
    void setIcon(QString path, int w = 50, int h = 50);
    bool isSelected();
    void setSelected(bool f);
    void setSize(int w, int h);

protected:
    void mousePressEvent(QMouseEvent *);

signals:
    void clicked(GestureIcon *p);

private:
    QPixmap gesture;
    bool selected;

};

#endif // GESTUREICON_H
