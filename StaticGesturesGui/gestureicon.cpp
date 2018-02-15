#include "gestureicon.h"
#include <QDebug>

GestureIcon::GestureIcon(QWidget *parent) : QLabel (parent)
{

}

void GestureIcon::setIcon(QString path, int w, int h)
{
    gesture = QPixmap(path);
    this->setFixedWidth(w);
    this->setFixedHeight(h);
    setPixmap(gesture.scaled(w, h));
    selected = false;
}

void GestureIcon::setSize(int w, int h)
{
    this->setFixedWidth(w);
    this->setFixedHeight(h);
    setPixmap(gesture.scaled(w, h));
}

bool GestureIcon::isSelected()
{
    return selected;
}

void GestureIcon::setSelected(bool f)
{
    selected = f;
}
void GestureIcon::mousePressEvent(QMouseEvent *)
{
    emit clicked(this);
}
