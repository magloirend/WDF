
@app.get("/matching_products/")
def get_matching_products(query):
	df = pd.read_csv('/home/victordedalus/code/magloirend/WDF/raw_data/new_products_metadata_df.csv')
	answer = dummy_model(df, query)
	return answer
	if type(answer) == str:
		return answer
	else:
		dict_answer = answer.to_dict('index')
		return dict_answer

if __name__ == '__main__':
	query = input("Que cherchez-vous ? \n")
	print(get_matching_products(query))
	print(type(get_matching_products(query)))
