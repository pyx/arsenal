"""arsenal.forum - forum blueprint"""

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import NewPostForm, NewTopicForm, UpdatePostForm
from .models import Post, Topic, db


forum = Blueprint(
    'forum', __name__, template_folder='templates', static_folder='static')


@forum.route('/', methods=['GET', 'POST'])
@login_required
def index():
    topics = Topic.query.order_by(Topic.updated_on.desc())
    form = NewTopicForm()
    if form.validate_on_submit():
        topic = Topic(title=form.title.data, author=current_user)
        post = Post(topic=topic,
                    author=current_user,
                    content=form.content.data)
        post.update_html()
        db.session.add(topic)
        db.session.add(post)
        db.session.commit()
        flash('New topic created')
        return redirect(topic.url)
    return render_template('forum/index.html', topics=topics, form=form)


@forum.route('/<int:id>/', methods=['GET', 'POST'])
@login_required
def topic(id):
    topic = Topic.query.get_or_404(id)
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post(topic=topic,
                        author=current_user,
                        content=form.content.data)
        new_post.update_html()
        db.session.add(new_post)
        db.session.flush()
        topic.updated_on = new_post.created_on
        db.session.commit()
        flash('New post submitted')
        anchor = 'post-%d' % topic.posts.count()
        return redirect(url_for('.topic', id=topic.id, _anchor=anchor))
    return render_template('forum/topic.html', topic=topic, form=form)


@forum.route('/edit/<int:num>/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_post(num, id):
    post = Post.query.get_or_404(id)
    if post.author.id != current_user.id:
        abort(401)
    form = UpdatePostForm(obj=post)
    if form.validate_on_submit():
        post.content = form.content.data
        post.update_html()
        post.topic.updated_on = post.updated_on
        db.session.add(post)
        db.session.add(post.topic)
        db.session.commit()
        flash('Post updated')
        anchor = 'post-%d' % num
        return redirect(url_for('.topic', id=post.topic_id, _anchor=anchor))
    return render_template('forum/edit_post.html', form=form)
