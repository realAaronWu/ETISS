/**

@copyright

<pre>

	Copyright (c) 2014 Institute for Electronic Design Automation, TU Munich

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.

</pre>

@author Marc Greim <marc.greim@mytum.de>

@date December 15, 2014

@version 0.4

*/
/**
	@file

	@brief contains the stressor class that loads and activates faults.

	@detail

*/

#ifndef ETISS_STRESSOR_H_
#define ETISS_STRESSOR_H_

#ifndef NO_ETISS
#include "etiss/fault/Fault.h"
#else
#include "fault/Fault.h"
#endif



namespace etiss{

namespace fault{

class Stressor{
public:

	static bool loadXML(const std::string & file);
	static bool addFault(const Fault & f);

    /**
        @return true if the fired trigger expired
    */
    static bool firedTrigger(const Trigger & firedTrigger,int32_t fault_id,Injector * injector,uint64_t time_ps);
	static void clear();

};

}

}


#endif
