def Paginator(page, total_count, page_size):
	max_page = (total_count - 1) // page_size + 1
	if max_page < 1:
		max_page = 1

	if page:
		page = int(page)
	else:
		page = 1
	if page < 1:
		page = 1

	if page >= max_page:
		next_page = False
	else:
		next_page = page + 1

	if page <= 1:
		prev_page = False
	elif page > max_page:
		prev_page = max_page
	else:
		prev_page = page - 1

	start = (page - 1) * page_size
	end = start + page_size
	# print(page, max_page, next_page, prev_page, start, end)
	return (page, max_page, next_page, prev_page, start, end)