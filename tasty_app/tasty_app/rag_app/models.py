from django.db import models

# 음식 정보 저장 모델
class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name="음식명")
    description = models.TextField(verbose_name="설명")  # 긴 텍스트 저장
    price = models.DecimalField(models.IntegerField(verbose_name="가격"))
    category = models.CharField(max_length=50, verbose_name='카테고리')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

# Django 모델의 메타데이터(추가 설정) 정의
class Meta:
    verbose_name = "음식"            # 단수형 이름 한글로 지정
    verbose_name_plural = "음식들"   # 복수형 이름 한글로 지정
    ordering = ['-created_at']      # 모델 객체들을 정렬(내림차순(최신순))

def __str__(self):
    return self.name
