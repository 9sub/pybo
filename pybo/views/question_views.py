from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question




@login_required(login_url='common:login') # 어노테이션 이용시 자동으로 로그인 화면으로 이동
def question_create(request):
    if request.method=='POST': #post 방식
        form=QuestionForm(request.POST) #인수 = request.POST
        if form.is_valid(): #폼이 유효하면
            question=form.save(commit=False) #임시 저장해 question 객체를 받음 , commit=False 는 임시저장을 뜻함
            question.author = request.user
            question.create_date=timezone.now() #실제 저장을 위해 작성일시 설정
            question.save() #데이터 실제로 저장
            return redirect('pybo:index')
    else: #GET 방식
        form=QuestionForm()
    context={'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_modify(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request,'수정권한이 없습니다')#메세지 모듈을 이용해 오류 발생시키기
        return redirect('pybo:detail',question_id=question.id)
    if request.method=="POST": # 수정된 내용이 반영 되야함
        form=QuestionForm(request.POST,instance=question)# instance를 기준으로 폼을 생성하지만 덮어써라
        if form.is_valid():
            question=form.save(commit=False)
            question.modify_date=timezone.now()
            question.save()
            return redirect('pybo:detail',question_id=question.id)
    else: # get 방식
        form=QuestionForm(instance=question)# 폼의 속성값이 instance 값으로 채워짐
    context={'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_delete(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.user !=question.author:
        messages.error(request,'삭제권한이 없습니다')
        return redirect('pybo:detail',question_id=question.id)
    question.delete()
    return redirect('pybo:index')
@login_required(login_url='common:login')
def question_vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.user == question.author:
        messages.error(request,'본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)