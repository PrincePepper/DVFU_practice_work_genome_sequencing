# Sequences filter 🧬

Проект по фильтрации данных **секвенатора генома**  для Тихоокеанского института биоорганической химии им. Г.Б. Елякова
ДВО РАН в пределах практики

## Место и период прохождения практики:

Лаборатория морской биохимии Тихоокеанского института биоорганической химии им. Г.Б. Елякова ДВО РАН проводит
исследования по секвенированию и анализу генов и геномов макро- и микроорганизмов, выделению, установлению структур и
активностей ферментов и их комплексов. На базе лаборатории имеется секвенатор MiSeq, Illumina (генетический анализатор)
для проведения высокопроизводительного секвенирования геномов, метагеномов, ампликонов.

## Техническое задание

Разработка приложения, предназначенного для автоматизации отделения (фильтрации) некачественных прочтений.

1. Определить требования к новому решению;
2. Разработать архитектуру проекта;
3. Разработать необходимое приложение для удаления (фильтрации) некачественных прочтений.

## Чуть чуть теории

**Секвенирование** (от англ. sequence — «последовательность») — это общее название методов, которые позволяют установить
последовательность нуклеотидов в молекуле ДНК. В результате секвенирования получают формальное описание первичной
структуры линейной макромолекулы в виде последовательности мономеров в текстовом виде.  
*Принцип секвенирования* основан на технологии Solexa, включающей обогащение методом bridge-ПЦР на проточном чипе,
секвенирование методом синтеза (SBS) с использованием флуоресцентно-меченных нуклеотидов и детекцию света флуоресценции
от кластеров ДНК.

## Структура проекта

```
├── desktop - главный файл
│   ├── cut.awk
│   ├── filter.sh
│   ├── icons
│   ├── main.py - это запускать
│   ├── main_window.py - а сюда не лазить :)
├── misc
│   └── cut_sequence_script.py - скрипт для удобной вырезки сегмента
├── requirements.txt - зависимости
├── shell - файлы старых и актульных версий Shell и awk кода
```

***The project was released for our University course***

## Ответственные за проект

- [Александр Пищиков](https://github.com/AlexPishchikov)
- [Семен Середа](https://github.com/PrincePepper)
- [Станислав Нагорнов](https://github.com/praisethedeviI)
- [Жильцов Дмитрий](https://github.com/dmzpp)
