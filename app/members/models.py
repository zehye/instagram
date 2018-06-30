from django.contrib.auth.models import AbstractUser
from django.db import models

from members.exceptions import RelationNotExist, DuplicateRelationException
from posts.models import Post


class User(AbstractUser):
    CHOICES_GENDER = (
        ('M', '남성'),
        ('F', '여성'),
        ('x', '선택안함'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    to_relation_users = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='from_relation_users',
        related_query_name='from_relation_user',
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.username

    def follow(self, to_user):
        if self.relations_by_from_user.filter(to_user=to_user).exists():
            raise DuplicateRelationException(
                from_user=self,
                to_user=to_user,
                relation_type='follow'
            )
        else:
            return self.relations_by_from_user.create(
                to_user=to_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
            )

    def unfollow(self, to_user):
        q = self.relations_by_from_user.filter(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )
        if q:
            q.delete()
        else:
            raise RelationNotExist(
                from_user=self,
                to_user=to_user,
                relation_type='Follow'
            )

    @property
    def following(self):
        # 내가 follow중인 User QuerySet 리턴
        # return User.objects.filter(
        #     pk__in=Relation.objects.filter(
        #         from_user=self,
        #         relation_type='f',
        #     ).values('to_user')
        # )
        # return User.objects.filter(pk__in=self.following_relations.values('to_user'))
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    @property
    def followers(self):
        # 나를 follow중인 User QuerySet리턴
        # return User.objects.filter(pk__in=self.follower_relations.values('to_user'))
        return User.objects.filter(
            relations_by_from_user__to_user=self,
            relations_by_from_user__relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    @property
    def block_users(self):
        # 나를 follow중인 User QuerySet리턴
        # return User.objects.filter(pk__in=self.block_relations.values('to_user'))
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_BLOCK
        )

    @property
    def following_relations(self):
        # 내가 follow중인 Relation Query리턴

        # 역참조 되는 manager객체
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW)

    @property
    def follower_relations(self):
        # 나를 follow중인 Relation Query리턴
        return self.relation_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW)

    @property
    def block_relations(self):
        # 내가 block한 Relation Query 리턴
        return self.relation_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_BLOCK)


class Relation(models.Model):
    """
    User간의 MTM연결 중개 테이블
    """
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_FOLLOW = 'f'
    CHOICES_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'Follow'),
        (RELATION_TYPE_BLOCK, 'block'),
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_from_user',
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user',
    )

    relation_type = models.CharField(
        max_length=1,
        choices=CHOICES_RELATION_TYPE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} ({type})'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display(),
        )
