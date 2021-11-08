from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]


# TODO Implement content models, link to wagtail

"""
package invites

import "time"

// TODO: tags
//    standard tag: WELCOME_CONTENT (must be there)
//  standard tag: RECOMMENDED (must be there)
//  other possible tags: EXERCISE, DIET
//  each client type (from the client profile) can be a tag, to be used for targeting
//        e.g to allow pushing / notifying specific individuals when an item is posted
//    gender (Male, Female) can be used as OPTIONAL tags
//  topics (decided by editors) can be added as tags

// TODO: this assumes a simple assets service that we can post files to & link from
// TODO: ensure links (e.g images) in content that we stage here are cacheable
//    this might involve proxying and rewriting them
// TODO: downsize large images etc
// TODO: consider: content to show during onboarding

type Content struct {
    ID           string
    Title        string
    Body         string // TODO: standardize format e.g HTML or MD
    Author       string
    AuthorAvatar string // TODO: Link; ensure this avatar is cacheable (e.g ETags)
    HeroImage    string // TODO: optional; e.g videos may not have one; also make cacheable
    ContentType  string // TODO: enum e.g video, audio, article
    PublicLink   string // a link safe for sharing e.g a link on the CMS

    CreatedAt time.Time
    UpdatedAt time.Time
    Active    bool

    // e.g estimated time to read an article or video/audio length
    Estimate int // TODO: standardize unit e.g seconds

    // tags are used to filter and target content
    // some tags are standard (prescribed )
    Tags []string

    // calculated fields that are updated and cached
    LikeCount     int
    BookmarkCount int
    ShareCount    int
    ViewCount     int
}

type ContentLikes struct {
    ID string

    UserID    string // TODO FK
    ContentID string // TODO FK

    // TODO: composite index, unique together, userID and contentID
}

type ContentBookmarks struct {
    ID string

    UserID    string // TODO FK
    ContentID string // TODO FK

    // TODO: composite index, unique together, userID and contentID
}

type ContentShares struct {
    ID string

    UserID    string // TODO FK
    ContentID string // TODO FK
    Channel   string // TODO enum

    // TODO: composite index, unique together, userID and contentID
}

type FetchCMSContent interface {
    // FetchCMSContent synchronizes content from Ghost CMS
    // and is triggered by a scheduled job OR on demand.
    //
    // The scheduled job should limit itself to recent content e.g
    // last 24 hours.
    //
    // For initial setup, this can be called manually with no `since`
    // parameter to synchronize all content.
    FetchCMSContent(
        since *time.Time,
    ) (bool, error)
}

type ILikeContent interface {
    // TODO: update like count (increment)
    // TODO: idempotence, with user ID i.e a user can only like once
    // TODO: add / check entry in ContentLikes table
    // TODO: metrics
    LikeContent(
        userID string,
        contentID string,
    ) (bool, error)
}

type IUnlikeContent interface {
    // TODO: update like count (decrement)
    // TODO: idempotence, with user ID i.e a user can only unlike something they liked
    // TODO: remove entry from ContentLikes table if it exists...be forgiving (idempotence)
    // TODO: metrics
    UnlikeContent(
        userID string,
        contentID string,
    ) (bool, error)
}

type IBookmarkContent interface {
    // TODO: update bookmark count (increment)
    // TODO: idempotence, with user ID i.e a user can only bookmark once
    // TODO: add / check entry in ContentBookmarks table
    // TODO: metrics
    BookmarkContent(
        userID string,
        contentID string,
    ) (bool, error)
}

type IUnbookmarkContent interface {
    // TODO: update bookmark count (decrement)
    // TODO: idempotence, with user ID i.e a user can only remove something they bookmarked
    // TODO: remove entry from ContentBookmarks table if it exists...be forgiving (idempotence)
    // TODO: metrics
    UnbookmarkContent(
        userID string,
        contentID string,
    ) (bool, error)
}

type IShareContent interface {
    // TODO: update share count (increment)
    // TODO: add / check entry in ContentShares table
    // TODO: metrics
    ShareContent(
        userID string,
        contentID string,
        channel string,
    ) (bool, error)
}

type IGetContent interface {
    // TODO Update view metrics each time a user views a piece
    // TODO Increment view count, idempotent
    Get(userID string, contentID string) (*Content, error)
}

type IInactivateContent interface {
    // TODO Idempotent
    // TODO Auditable
    Inactivate(contentID string) (*Content, error)
}

type IGetRecommendedContent interface {
    // TODO: initial implementation can simply use tags i.e recommend items with similar
    // tags to the item that is listed
    // TODO: limit only to active content
    // TODO: default to sorting in reverse chronological order (i.e most recent first)
    GetRecommended(contentID string, limit int) ([]*Content, error)
}

// TODO: this is for listing / querying
type IFetchContent interface {
    // TODO: limit only to active content
    // TODO: default to sorting in reverse chronological order (i.e most recent first)
    Fetch(
        limit int, // number to fetch, if zero limit to 5
        tags []string, // optional; if tags are supplied, combine them with AND
    ) ([]*Content, error)
}
"""
