# version 0.1 16 sep 2021

def povBasico(comment=""):
    cad = "#version 3.7;\n\n"
    cad += "// PovBasico Marcelo PM Noviembre 2016\n"
    cad += cad + comment
    cad += "global_settings{ assumed_gamma 1.0 }\n"
    cad += "default{ finish{ ambient 0.1 diffuse 0.9 }}\n"
    cad += "background {color rgb <0.1, 0.1, 0.1>}\n\n"
    return cad


def povCamara(locx, locy, locz, lookx, looky, lookz):
    location = "<" + str(locx) + "," + str(locy) + "," + str(locz) + ">\n"
    look = "<" + str(lookx) + "," + str(looky) + "," + str(lookz) + ">"
    cad = "camera{\n" + "   location " + location
    cad += "   look_at " + look + "}\n\n"
    return cad


def povLuz(locx, locy, locz, r, g, b):
    loc = "<" + str(locx) + ", " + str(locy) + ", " + str(locz) + ">"
    color = "color rgb <" + str(r) + ", " + str(g) + ", " + str(g) + ">}\n"
    cad = "light_source {" + loc + color + "\n"
    return cad


def povEsfera(locx, locy, locz, radio, texture="default"):
    if texture == "default":
        texture = "texture{pigment{color rgb <1.0, 1.0, 1.0>}}"
    loc = "<" + str(locx) + ", " + str(locy) + ", " + str(locz) + ">, " + str(radio)
    cad = "sphere {" + loc + " " + texture + "}\n"
    return cad


def povCilindro(x1, y1, z1, x2, y2, z2, radio, texture="default"):
    if texture == "default":
        texture = "texture{pigment{color rgb <1.0, 1.0, 1.0>}}"
    loc1 = "<" + str(x1) + ", " + str(y1) + ", " + str(z1) + ">"
    loc2 = "<" + str(x2) + ", " + str(y2) + ", " + str(z2) + ">," + str(radio) + " "
    cad = "cylinder {" + loc1 + loc2 + " " + texture + "}\n"
    return cad


def povPigmento(r, g, b):
    cad = "<" + str(r) + "," + str(g) + "," + str(b) + ">"
    cad = "pigment {color rgb " + cad + "}"
    return cad


def povPigmentosBasicos():
    cad = "#declare trojo = pigment {color rgb <1, 0, 0>}\n"
    cad += "#declare tverde = pigment {color rgb <0, 1, 0>}\n"
    cad += "#declare tazul = pigment {color rgb <0, 0, 1>}\n\n"

    return cad


def povEjes(size, radio):
    tr = " texture{tred}"
    tg = " texture{tgreen}"
    tb = " texture{tblue}"
    cad = "// Axes \n"
    cad += "povCylinder(0.0, 0.0, 0.0", str(size), "0.0, 0.0,", radio, tr
    cad += "povCylinder(0.0, 0.0, 0.0, 0.0", str(size), " 0.0", radio, tg
    cad += "povCylinder(0.0, 0.0, 0.0, 0.0", "0.0,", str(size), radio, tb
    return cad


def povPiso(num=0):
    cad = ""
    if (num == 0):
        cad = "plane { <0,1,0>, 0  hollow \n" \
              "texture{ pigment{ color rgb<0.35,0.60, 0.00> }\n" \
              "         normal { bumps 0.25 scale 0.05 }" \
              "         finish { phong 1 }" \
              "       }} "
    return cad


def povTextura(num=0):
    cad = "#declare t0 = texture{pigment color rgb<1.0, 0.0, 0.0>}"
    if (num == 1):  # textura madera cherry
        cad = "#declare t1 =\n" \
              "pigment {wood turbulence 0.3\n" \
              "color_map {\n" \
              "[0.8 rgb <0.66, 0.31, 0.20>]\n" \
              "[0.8 rgb <0.40, 0.13, 0.06>]\n" \
              "[1.0 rgb <0.20, 0.06, 0.03>]}}\n\n"
    elif (num == 2):  # textura de pino
        cad = "#declare t2 = pigment { wood turbulence 0.2\n" \
              "color_map {\n" \
              "[0.8 rgb <1.0, 0.72, 0.25>]\n" \
              "[0.8 rgb <0.5, 0.50, 0.06>]\n" \
              "[1.0 rgb <0.4, 0.40, 0.03>]}}\n\n"
    elif (num == 3):  # vidrio verde
        cad = "#declare t3 =\n" \
              "texture {\n" \
              "pigment { rgbf <0.18, 0.98, 0.18, 0.9> }\n" \
              "finish  {\n" \
              "ambient 0.1\n" \
              "diffuse 0.1\n" \
              "reflection 0.1\n" \
              "specular 0.8\n" \
              "roughness 0.0003\n" \
              "phong 1\n" \
              "phong_size 400}}\n\n"
    elif (num == 4):  # metal
        cad = "#declare t4 = texture{pigment{color rgb <0.94, 0.03, 0.090>}\n" \
              "finish {\n ambient 0.35\n   brilliance 2\n" \
              "diffuse 0.3\n   metallic\n   specular 0.80\n" \
              "   roughness 1/20\n   reflection 0.1}}\n\n"
    return cad
