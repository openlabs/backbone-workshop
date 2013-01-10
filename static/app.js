$(document).ready(function() {
  var app = {};
  
  app.FeedItem = Backbone.Model.extend({
    getColor: function() {
      return 'blue';
    },
  });
  app.FeedItemView = Backbone.View.extend({
    initialize: function() {
      this.model.on("change", this.render, this);
    }, 
    tagName: 'tr',
    template: _.template($("script#feeditem").html()),
    render: function() {
      this.$el.html(this.template({
        feed_item: this.model
      }));
      return this;
    },
    events: {
      "click span.message": "allowEdit",
      "click button": "save"
    },
    allowEdit: function(event) {
      this.$("span.message").hide();
      this.$(".edit-mode").show();
    },
    save: function(event) {
      this.model.set('message', this.$('input').val());
      this.model.save();
    }
  });
  app.NewsFeed = Backbone.Collection.extend({
    model: app.FeedItem,
    url: '/news-feed/',
    parse: function(response) {
      return response.result;
    }
  })

  window.app = app;

  app.news_feed = new app.NewsFeed;
  app.news_feed.fetch({
    success: function(collection, response, options) {
      _.each(collection.models, function(model) {
        v = new app.FeedItemView({model: model});
        $("table#feeds").append(v.render().el);
      });
    }
  })
    
});
