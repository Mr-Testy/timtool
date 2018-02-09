from .models import ABCTune, Tune, Title
from django.template.defaultfilters import slugify
from django.contrib import messages
from os import remove, rename
from subprocess import run
from django.core import serializers
from django.db.models import Q


def handle_uploaded_file(file, request):
    content = file.readlines()
    all_abc = []
    flag = False
    for line in content:
        if not flag:
            line = line.decode("UTF-8").strip("\r\n")
            line = line.split(":")
            if line[0] == "X":
                all_abc.append(ABCTune(X=int(line[1])))
            elif line[0] == "T":
                if all_abc[-1].T == "":
                    all_abc[-1].T = line[1]
                elif all_abc[-1].other_title == "":
                    all_abc[-1].other_title = line[1]
                elif all_abc[-1].other_title2 == "":
                    all_abc[-1].other_title2 = line[1]
            elif line[0] == "R":
                all_abc[-1].R = line[1]
            elif line[0] == "C":
                if all_abc[-1].C == "":
                    all_abc[-1].C = line[1]
                elif all_abc[-1].other_composer == "":
                    all_abc[-1].other_composer = line[1]
                elif all_abc[-1].other_composer2 == "":
                    all_abc[-1].other_composer2 = line[1]
            elif line[0] == "S":
                all_abc[-1].S = line[1]
            elif line[0] == "H":
                all_abc[-1].H = all_abc[-1].H + "\r\n" + line[1]
            elif line[0] == "N":
                all_abc[-1].N = all_abc[-1].N + "\r\n" + line[1]
            elif line[0] == "D":
                all_abc[-1].D = all_abc[-1].D + "\r\n" + line[1]
            elif line[0] == "Z":
                all_abc[-1].Z = line[1]
            elif line[0] == "M":
                all_abc[-1].M = line[1]
            elif line[0] == "L":
                all_abc[-1].L = line[1]
            elif line[0] == "Q":
                all_abc[-1].Q = line[1]
            elif line[0] == "K":
                all_abc[-1].K = line[1]
                flag = True
        else:
            line = line.decode("UTF-8")
            if len(line) > 4:
                if line[0] == "W":
                    all_abc[-1].W = all_abc[-1].W + "\r\n" + line[1]
                else:
                    all_abc[-1].content = all_abc[-1].content + line
            else:
                flag = False

    for abc in all_abc:
        if abc.T and abc.K and abc.R and abc.content:
            slug = slugify(abc.T + "-" + abc.K + "-" + abc.R)
            if abc.other_title:
                slug2 = slugify(abc.other_title + "-" + abc.K + "-" + abc.R)
            else:
                slug2 = ""
            if abc.other_title2:
                slug3 = slugify(abc.other_title2 + "-" + abc.K + "-" + abc.R)
            else:
                slug3 = ""
            titles = Title.objects.filter(Q(slug=slug) | Q(slug=slug2) | Q(slug=slug3))

            if titles.count()>0:
                # messages.warning(request, "le tune " + slug + " existe déjà")
                messages.warning(request, serializers.serialize("json", [abc, ]))
                for title in titles:
                    messages.error(request, title.slug)
                    tune = Tune.objects.get(slug=title.slug)
                    messages.info(request, serializers.serialize("json", [tune, ]))
                # messages.info(request, serializers.serialize("json", [tune, ]))
            else:
                tune = Tune()
                tune.name = abc.T
                tune.key = abc.K
                tune.type = abc.R
                tune.description = abc.H
                tune.added_by = request.user
                tune.save()
                abc.tune = tune
                abc.save()
                title = Title(name=abc.T, slug=slug)
                title.save()
                title.belong_to_tunes.add(tune)
                if abc.other_title:
                    title2 = Title(name=abc.other_title, slug=slug2)
                    title2.save()
                    title2.belong_to_tunes.add(tune)
                if abc.other_title2:
                    title3 = Title(name=abc.other_title2, slug=slug3)
                    title3.save()
                    title3.belong_to_tunes.add(tune)
                messages.success(request, "le tune " + tune.slug + " a bien été créé")
        else:
            messages.error(request, "abc incomplet ou erroné")


def handle_text_area(str, request):
    content = str.splitlines(True)
    all_abc = []
    flag = False
    for line in content:
        if not flag:
            line = line.strip("\r\n")
            line = line.split(":")
            if line[0] == "X":
                all_abc.append(ABCTune(X=int(line[1])))
            elif line[0] == "T":
                if all_abc[-1].T == "":
                    all_abc[-1].T = line[1]
                elif all_abc[-1].other_title == "":
                    all_abc[-1].other_title = line[1]
                elif all_abc[-1].other_title2 == "":
                    all_abc[-1].other_title2 = line[1]
            elif line[0] == "R":
                all_abc[-1].R = line[1]
            elif line[0] == "C":
                if all_abc[-1].C == "":
                    all_abc[-1].C = line[1]
                elif all_abc[-1].other_composer == "":
                    all_abc[-1].other_composer = line[1]
                elif all_abc[-1].other_composer2 == "":
                    all_abc[-1].other_composer2 = line[1]
            elif line[0] == "S":
                all_abc[-1].S = line[1]
            elif line[0] == "H":
                all_abc[-1].H = all_abc[-1].H + "\r\n" + line[1]
            elif line[0] == "N":
                all_abc[-1].N = all_abc[-1].N + "\r\n" + line[1]
            elif line[0] == "D":
                all_abc[-1].D = all_abc[-1].D + "\r\n" + line[1]
            elif line[0] == "Z":
                all_abc[-1].Z = line[1]
            elif line[0] == "M":
                all_abc[-1].M = line[1]
            elif line[0] == "L":
                all_abc[-1].L = line[1]
            elif line[0] == "Q":
                all_abc[-1].Q = line[1]
            elif line[0] == "K":
                all_abc[-1].K = line[1]
                flag = True
        else:
            if len(line) > 4:
                if line[0] == "W":
                    all_abc[-1].W = all_abc[-1].W + "\r\n" + line[1]
                else:
                    all_abc[-1].content = all_abc[-1].content + line
            else:
                flag = False

    for abc in all_abc:
        if abc.T and abc.K and abc.R and abc.content:
            try:
                slug = slugify(abc.T + "-" + abc.K + "-" + abc.R)
                tune = Tune.objects.get(slug=slug)
                messages.warning(request, "le tune " + slug + " existe déjà")
            except Tune.DoesNotExist:
                abc.save()
                tune = Tune()
                tune.name = abc.T
                tune.key = abc.K
                tune.type = abc.R
                tune.description = abc.H
                tune.added_by = request.user
                tune.abc = abc
                tune.save()
                messages.success(request, "le tune " + tune.slug + " a bien été créé")
        else:
            messages.error(request, "abc incomplet ou erroné. Les champs T: (titre), K: (tonalité) et R: (type) sont obligatoires")


def constructABC_from_tune(tune, path, temp_path):
    file = open(str(temp_path), 'w')
    file.write("X:" + str(tune.id) + "\n")
    if tune.abc.T:
        file.write("T:" + tune.abc.T + "\n")
    if tune.abc.other_title:
        file.write("T:" + tune.abc.other_title + "\n")
    if tune.abc.other_title2:
        file.write("T:" + tune.abc.other_title2 + "\n")
    if tune.abc.R:
        file.write("R:" + tune.abc.R + "\n")
    if tune.abc.C:
        file.write("C:" + tune.abc.C + "\n")
    if tune.abc.other_composer:
        file.write("C:" + tune.abc.other_composer + "\n")
    if tune.abc.other_composer2:
        file.write("C:" + tune.abc.other_composer2 + "\n")
    if tune.abc.Z:
        file.write("Z:" + tune.abc.Z + "\n")
    if tune.abc.N:
        file.write("N:" + tune.abc.N + "\n")
    if tune.abc.M:
        file.write("M:" + tune.abc.M + "\n")
    if tune.abc.L:
        file.write("L:" + tune.abc.L + "\n")
    if tune.abc.Q:
        file.write("Q:" + tune.abc.Q + "\n")
    if tune.abc.K:
        file.write("K:" + tune.abc.K + "\n")
    file.write(tune.abc.content)
    if tune.abc.W:
        file.write("W:" + tune.abc.W + "\n")
    file.close()
    with open(str(temp_path), 'r+') as infile, open(str(path), 'w') as outfile:
        for line in infile:
            if not line.isspace():
                outfile.write(line)
    remove(str(temp_path))


def constructSVG_from_ABC(path_abc, path_svg):
    run(["abcm2ps", "-g", str(path_abc), "-O", str(path_svg)])
    rename(str(path_svg).replace(".svg", "001.svg"), str(path_svg))


def constructMIDI_from_ABC(path_abc, path_midi):
    run(["abc2midi", str(path_abc), "-o", str(path_midi)])
