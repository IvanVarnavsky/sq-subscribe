from celery.task import task
from sq_subscribe.mailqueue.models import create_mailqueue
from sq_subscribe.subscribe.models import Subscribe, UserSubscribes


@task
def build_subsribe_query(subscribe_id=None):
    try:
        subscribe = Subscribe.objects.get(id = subscribe_id)
    except Exception:
        raise Exception('Subscribe not found')
    # TODO сделать из переменных сообщения актуальные данные (если подписка на контент)
    usersubscribes = UserSubscribes.objects.filter(subscribe = subscribe)
    for usersub in usersubscribes:
        # TODO добавить в сообщение userdata
        create_mailqueue(subject=subscribe.subject,template=subscribe.template,send_to=usersub.user.email,
                         content_type=subscribe.content_type,message=subscribe.message)


