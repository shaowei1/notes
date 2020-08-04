result = (
        session.query(Work).
        options(
            joinedload(Work.company_users).
            joinedload(CompanyUser.user)
        ).
        filter(Work.id == 1).
        filter(User.first_name == 'The name').  <<--- I can't get this to work.
        all()
    )


    session.query(Work).\
        join(Work.company_users).\
        join(CompanyUser.user).\
        filter(Work.id == 1).\
        filter(User.first_name == 'The name').\
        all()

    session.query(Work).\
        join(Work.company_users).\
        join(CompanyUser.user).\
        options(contains_eager(Work.company_users).
                contains_eager(CompanyUser.user)).\
        filter(Work.id == 1).\
        filter(User.first_name == 'The name').\
        all()


        The reason it is not working is that joinedload (and all the other relationship loading techniques) are meant to be entirely transparent. That is to say having a joinedload in your query should not affect it in any other way other than resulting in the relationships being filled. You should read "The Zen of Joined Eager Loading", which begins with:

        Since joined eager loading seems to have many resemblances to the use of Query.join(), it often produces confusion as to when and how it should be used. It is critical to understand the distinction that while Query.join() is used to alter the results of a query, joinedload() goes through great lengths to not alter the results of the query, and instead hide the effects of the rendered join to only allow for related objects to be present.

        One of the tricks is to use aliases for the joined tables which are not made available. Your query then ends up performing an implicit cross-join between Work and User, and hence the extra rows. So in order to filter against a joined table, use Query.join():

        and if you also need the eagerloads in place, you can instruct the Query that it already contains the joins with contains_eager():

        Note the chained calls to contains_eager().
