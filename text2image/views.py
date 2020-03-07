from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import ctypes
import subprocess
import sys

# Create your views here.

def generate(request):
    sentence = request.GET.get("sentence", "")
    word = request.GET.get("highlight", "")
    dataset = request.GET.get("dataset", "COCO")
    if sentence == "":
        return f""

    with open("/home/ubuntu/text2image/ControlGAN/data/%s/example.txt"%("birds" if dataset=="CUB" else "coco"), "w") as f_ex:
        f_ex.write(sentence)
    yml_path = "cfg/eval_bird.yml" if dataset == "CUB" else "cfg/eval_coco.yml"
    if word != "":
        highlight = sentence.split(' ').index(word)
    else:
        highlight = 0
    h = ctypes.c_size_t(hash((sentence, word, dataset))).value
    p = subprocess.Popen("python main.py --cfg %s --gpu 0 --output_file_name ../gen/%d --highlight %d"%(yml_path, h, highlight),
        cwd="/home/ubuntu/text2image/ControlGAN/code", stdout=sys.stdout, stderr=sys.stderr, shell=True).communicate()
    if word != "":
        return JsonResponse({
            "image_url": '/static/%d_1.jpg'%(h)
        })
    else:
        return JsonResponse({
            "image_url": "/static/%d_0.png"%(h)
        })

