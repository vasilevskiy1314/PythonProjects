from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all posts in selected category?')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input('Название категории: ')  # считываем подтверждение
        for category in Category.objects.filter(name=answer):
            print(category)
            if answer == Category.objects.get(name=answer).name:  # в случае подтверждения действительно удаляем все товары
                pk = Category.objects.get(name=answer).id
                Post.objects.filter(postCategory=pk).delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all posts in category {answer} !'))
                return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано