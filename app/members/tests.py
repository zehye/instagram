from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase

from members.exceptions import RelationNotExist, DuplicateRelationException

User = get_user_model()


class RelationTestCase(TransactionTestCase):

    def create_dummy_user(self, num):
        # num에 주어진 개수만큼 유저를 생성 및 리턴
        return [User.objects.create_user(username=f'u{x + 1}')
        for x in range(num)]

    def test_follow(self):
        """
        특정 User가 다른 User를 follow할 결우, 정상 작동하는 지 확인
        :return:
        """
        # 임의의 유저 2명 생성(u1, u2)
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u1이 u2를 follow하도록
        relation = u1.follow(u2)
        print(u1.following)
        # relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        # u1의 following에 u2가 포함되어있는 지 확인
        # following은 user queryset
        self.assertIn(u2, u1.following)
        # u1.following.filter(pk=u2.pk).exists()

        # u1의 following_relations에서 to_user가 u2인 Relation이 존재하는 지 확인
        self.assertTrue(u1.following_relations.filter(to_user=u2).exists())

        # relation이 u1.following_relations에 포함되어 있는지
        self.assertIn(relation, u1.following_relations)

    def test_follow_only_once(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u2로의 follow를 두 번 실행
        u1.follow(u2)
        # 두번째 실행에서는 IndegrityError가 발생할 것이다.
        with self.assertRaises(DuplicateRelationException):
            u1.follow(u2)

        # u1의 following이 하나인지 확인
        self.assertEqual(u1.following.count(), 1)

    def test_unfollow_if_follow_exist(self):
        # follow가 존재할때 지워지는 지 확인
        u1, u2 = self.create_dummy_user(2)

        # u1이 u2를 follow후 unfollow실행
        u1.follow(u2)
        u1.unfollow(u2)

        # u1의 following에 u2가 없어야 함
        self.assertNotIn(u2, u1.following)

    def test_unfollow_fail_if_follow_not_exist(self):
        # 위에가 통과함과 동시에 follow가 존재하면 실패해야 하는 함수
        u1, u2 = self.create_dummy_user(2)
        # 아래 코드는 올바르지 않으므로 exception이 발생해야 한다.
        with self.assertRaises(RelationNotExist):
            u1.unfollow(u2)
