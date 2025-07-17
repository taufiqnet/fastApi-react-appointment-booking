export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-12 items-center">
        {/* Left Side - Image */}
        <div className="hidden md:block">
          <img 
            src="https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=880&q=80" 
            alt="Doctors caring for patient in hospital"
            className="rounded-xl shadow-2xl object-cover h-full max-h-[600px] w-full"
          />
        </div>

        {/* Right Side - Content */}
        <div className="space-y-8 text-center md:text-left">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 leading-tight">
            Welcome to Our <span className="text-blue-600">Healthcare</span> Portal
          </h1>
          
          <p className="text-lg text-gray-600 max-w-lg">
            Book appointments with top specialists in just a few clicks. 
            Our easy-to-use platform connects you with healthcare professionals 
            when you need them most.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <a 
              href="/auth/login" 
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition duration-300 shadow-lg hover:shadow-xl"
            >
              Book an Appointment
            </a>
            <a 
              href="/doctors" 
              className="px-8 py-3 border-2 border-blue-600 text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition duration-300"
            >
              Find a Doctor
            </a>
          </div>

          <div className="pt-8">
            <div className="inline-flex items-center gap-4 bg-white p-4 rounded-lg shadow-md">
              <div className="flex -space-x-2">
                <img 
                  src="https://randomuser.me/api/portraits/women/44.jpg" 
                  className="w-10 h-10 rounded-full border-2 border-white" 
                  alt="Patient"
                />
                <img 
                  src="https://randomuser.me/api/portraits/men/32.jpg" 
                  className="w-10 h-10 rounded-full border-2 border-white" 
                  alt="Patient"
                />
                <img 
                  src="https://randomuser.me/api/portraits/women/68.jpg" 
                  className="w-10 h-10 rounded-full border-2 border-white" 
                  alt="Patient"
                />
              </div>
              <div className="text-left">
                <p className="text-sm font-medium text-gray-700">Trusted by 5000+ patients</p>
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                  ))}
                  <span className="text-xs ml-1">(4.9/5)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}