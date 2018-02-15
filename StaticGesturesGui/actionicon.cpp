#include "actionicon.h"

ActionIcon::ActionIcon(QWidget *parent) : QLabel (parent)
{

}

void ActionIcon::setSize(int w, int h)
{
    this->setFixedWidth(w);
    this->setFixedHeight(h);
}

void ActionIcon::mousePressEvent(QMouseEvent *)
{
    emit clicked(this);
}
